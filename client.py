import socket
import threading


class ChatClient:

    def __init__(self, host, port):

        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.socket.connect((host, port))

        self.messages = []
        self.running = True

    def send_message(self, message):

        if message == "":
            return

        try:
            self.socket.send(message.encode())
        except:
            self.running = False

    def receive_messages(self):

        while self.running:

            try:

                message = self.socket.recv(1024).decode()

                if not message:
                    break

                self.messages.append(message)

            except:

                break

    def start_receiving(self):

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
        except:
            pass