import tkinter as tk

from client import ChatClient
from layout import create_layout


HOST = "127.0.0.1"
PORT = 5000


# Connect to server
try:

    client = ChatClient(HOST, PORT)

except ConnectionRefusedError:

    print("Server is not running.")
    print("Please run server.py first.")

    exit()


# Send message
def send_message(message_box, chat_box):

    message = message_box.get()

    if message == "":
        return

    client.send_message(message)

    chat_box.insert(
        tk.END,
        "You: " + message + "\n"
    )

    message_box.delete(0, tk.END)


# Check messages received from server
def check_messages():

    messages = client.get_messages()

    for message in messages:

        chat_box.insert(
            tk.END,
            message + "\n"
        )

    if client.running:

        root.after(
            100,
            check_messages
        )


# Close window
def close_window():

    client.close()

    root.destroy()


# Create main window
root = tk.Tk()


# Create GUI
message_box, chat_box = create_layout(
    root,
    send_message
)


# Start receiving messages
client.start_receiving()


# Check for new messages
root.after(
    100,
    check_messages
)


# Close button
root.protocol(
    "WM_DELETE_WINDOW",
    close_window
)


# Start application
root.mainloop()