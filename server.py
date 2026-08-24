import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

clients = []


def send_to_all(message):
    for client in clients:
        try:
            client.send(message.encode())
        except:
            pass


def receive_from_client(client, address):

    while True:

        try:
            message = client.recv(1024).decode()

            if not message:
                break

            print("\nClient:", message)
            print("Server: ", end="", flush=True)

            # Send client message to other clients
            for other_client in clients:
                if other_client != client:
                    try:
                        other_client.send(
                            ("Client: " + message).encode()
                        )
                    except:
                        pass

        except:
            break

    if client in clients:
        clients.remove(client)

    client.close()

    print("\nClient disconnected:", address)


def accept_clients():

    while True:

        client, address = server.accept()

        clients.append(client)

        print("\nClient connected:", address)
        print("Total clients:", len(clients))

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