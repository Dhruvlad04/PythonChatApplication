import socket
import threading


class ChatClient:
    def __init__(self, host, port):
        # AF_INET selects IPv4 and SOCK_STREAM selects TCP, a reliable
        # two-way byte stream between this client and the server.
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        # connect() completes the client side of the TCP connection.
        self.socket.connect((host, port))

        self.messages = []
        # The receiver thread writes here while Tkinter reads it.
        self.messages_lock = threading.Lock()
        self.running = True

    def send_message(self, message):
        if message == "":
            return

        try:
            # sendall() handles partial sends for us.
            self.socket.sendall(message.encode())
        except OSError:
            self.running = False

    def receive_messages(self):
        # recv() blocks, so this method must run outside the GUI thread.
        while self.running:
            try:
                message = self.socket.recv(1024).decode()

                if not message:
                    break

                with self.messages_lock:
                    self.messages.append(message)
            except OSError:
                break

        self.running = False

    def start_receiving(self):
        # A daemon thread will not keep Python alive after the GUI closes.
        thread = threading.Thread(
            target=self.receive_messages
        )

        thread.daemon = True
        thread.start()

    def get_messages(self):
        # Copy and clear together so each message is displayed only once.
        with self.messages_lock:
            messages = self.messages.copy()
            self.messages.clear()

        return messages

    def close(self):
        # shutdown() wakes a blocking recv() before the socket is closed.
        self.running = False

        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        try:
            self.socket.close()
        except OSError:
            pass
