import tkinter as tk

from client import ChatClient
from layout import create_layout


HOST = "127.0.0.1"
PORT = 5000


def run_chat_window():
    # The client opens the TCP connection before the window is created. This
    # lets us show a useful message if server.py has not been started yet.
    try:
        client = ChatClient(HOST, PORT)
    except ConnectionRefusedError:
        print("Server is not running. Start server.py first.")
        return

    root = tk.Tk()

    def send_message(message_box, chat_box):
        message = message_box.get()
        if message == "":
            return

        client.send_message(message)
        chat_box.insert(tk.END, "You: " + message + "\n")
        message_box.delete(0, tk.END)

    message_box, chat_box = create_layout(root, send_message)

    # recv() is already running in ChatClient's background thread. Tkinter
    # must only update widgets from this main thread, so after() checks the
    # thread-safe message queue instead of reading the socket directly.
    def check_messages():
        for message in client.get_messages():
            chat_box.insert(tk.END, message + "\n")

        if client.running:
            # Returning to the event loop keeps the window responsive.
            root.after(100, check_messages)

    def close_window():
        client.close()
        root.destroy()

    client.start_receiving()
    root.after(100, check_messages)
    root.protocol("WM_DELETE_WINDOW", close_window)
    root.mainloop()


if __name__ == "__main__":
    run_chat_window()
