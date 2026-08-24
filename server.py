import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

clients = []
clients_lock = threading.Lock()


def send_to_all(message):
    # A client can disconnect while this loop is broadcasting.
    with clients_lock:
        connected_clients = clients.copy()

    for client in connected_clients:
        try:
            client.sendall(message.encode())
        except OSError:
            continue


def receive_from_client(client, address):
    # recv() blocks for this client, so every client needs its own thread.
    while True:

        try:
            message = client.recv(1024).decode()

            if not message:
                break

            print("\nClient:", message)
            print("Server: ", end="", flush=True)

            # Send client message to other clients
            with clients_lock:
                connected_clients = clients.copy()

            for other_client in connected_clients:
                if other_client != client:
                    try:
                        other_client.sendall(
                            ("Client: " + message).encode()
                        )
                    except OSError:
                        continue

        except OSError:
            break

    with clients_lock:
        if client in clients:
            clients.remove(client)

    client.close()

    print("\nClient disconnected:", address)


def accept_clients():
    # accept() blocks too, so it runs separately from the server input loop.
    while True:
        try:
            client, address = server.accept()
        except OSError:
            break

        with clients_lock:
            clients.append(client)

        print("\nClient connected:", address)
        with clients_lock:
            total_clients = len(clients)
        print("Total clients:", total_clients)

        thread = threading.Thread(
            target=receive_from_client,
            args=(client, address)
        )

        thread.daemon = True
        thread.start()

        print("Server: ", end="", flush=True)


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))

server.listen(5)

print("==============================")
print("      PYTHON CHAT SERVER")
print("==============================")
print("Server started")
print("IP:", HOST)
print("Port:", PORT)
print("Waiting for clients...")
print()

thread = threading.Thread(
    target=accept_clients
)

thread.daemon = True
thread.start()


# Server sends messages
while True:

    message = input("Server: ")

    if message == "":
        continue

    if message.lower() == "exit":

        send_to_all("SERVER: Server ended the chat.")

        break

    # Send server message to every client
    send_to_all(
        "SERVER: " + message
    )


for client in clients:
    client.close()

server.close()

print("Server closed.")