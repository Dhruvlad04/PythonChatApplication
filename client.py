import socket
import threading


class ChatClient:

    def __init__(self, host, port):

        # Create a TCP socket
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        try:
            # Connect the client to the server
            self.socket.connect((host, port))

            print("Connected to server.")

        except ConnectionRefusedError:
            print("Server is not running.")
            self.socket.close()
            raise

        except OSError as error:
            print("Connection error:", error)
            self.socket.close()
            raise

        self.messages = []
        self.running = True

    def send_message(self, message):

        try:
            # Convert text to bytes and send it
            self.socket.send(message.encode())

        except ConnectionResetError:
            print("Server closed the connection.")
            self.running = False

        except OSError as error:
            print("Send error:", error)
            self.running = False

    def receive_messages(self):

        while self.running:

            try:
                # Receive up to 1024 bytes
                data = self.socket.recv(1024)

                if not data:
                    print("Server disconnected.")
                    self.running = False
                    break

                # Convert bytes to text
                message = data.decode()

                self.messages.append(message)

            except ConnectionResetError:
                print("Server closed the connection.")
                self.running = False
                break

            except OSError as error:
                print("Receive error:", error)
                self.running = False
                break

    def start_receiving(self):

        # Run receiving in another thread
        thread = threading.Thread(
            target=self.receive_messages
        )

        thread.daemon = True
        thread.start()

    def get_messages(self):

        messages = self.messages.copy()

        self.messages.clear()

        return messages

    def close(self):

        self.running = False

        try:
            self.socket.close()
        except OSError as error:
            print("Error closing socket:", error)