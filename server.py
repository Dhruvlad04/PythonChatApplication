import socket
import threading

# Server IP address and port
HOST = "127.0.0.1"
PORT = 5000

# List to store connected clients
clients = []


# Send a message to all connected clients
def send_to_clients(message):
    for client in clients:
        try:
            client.send(message.encode())
        except ConnectionResetError:
            print("A client connection was closed.")
        except OSError as error:
            print("Socket error:", error)


# Receive messages from one client
def handle_client(client, address):

    print("Client connected:", address)

    while True:
        try:
            # Receive data from the client
            data = client.recv(1024)

            if not data:
                print("Client disconnected:", address)
                break

            message = data.decode()

            if message == "exit":
                print("Client left:", address)
                break

            print("Client:", message)

            # Send the message to other connected clients
            for other_client in clients:
                if other_client != client:
                    try:
                        other_client.send(
                            ("Client: " + message).encode()
                        )
                    except ConnectionResetError:
                        print("Could not send to a client.")
                    except OSError as error:
                        print("Socket error:", error)

        except ConnectionResetError:
            print("Connection was closed by the client.")
            break

        except OSError as error:
            print("Socket error:", error)
            break

    if client in clients:
        clients.remove(client)

    client.close()


# Create a TCP socket
server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

try:
    # Assign IP address and port to the server
    server_socket.bind((HOST, PORT))

    # Start listening for clients
    server_socket.listen(5)

    print("================================")
    print("       PYTHON CHAT SERVER")
    print("================================")
    print("Server started.")
    print("IP:", HOST)
    print("Port:", PORT)
    print("Waiting for clients...")
    print()

    # Accept clients continuously
    while True:

        try:
            # Accept a new client connection
            client, address = server_socket.accept()

            clients.append(client)

            print("Client connected:", address)
            print("Total clients:", len(clients))

            # Handle this client separately
            thread = threading.Thread(
                target=handle_client,
                args=(client, address)
            )

            thread.start()

        except OSError as error:
            print("Could not accept client:", error)
            break

except OSError as error:
    print("Could not start server:", error)

finally:
    for client in clients:
        client.close()

    server_socket.close()

    print("Server stopped.")