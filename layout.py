import tkinter as tk


def create_layout(root, send_function):

    # Set the window title
    root.title("Python Chat Application")

    # Set the window size
    root.geometry("600x500")

    # Area where messages are displayed
    chat_box = tk.Text(
        root,
        width=65,
        height=20
    )

    chat_box.pack(
        padx=10,
        pady=10
    )

    # Text box for entering a message
    message_box = tk.Entry(
        root,
        width=45
    )

    message_box.pack(
        pady=5
    )

    # Button used to send the message
    send_button = tk.Button(
        root,
        text="Send",
        command=lambda: send_function(
            message_box,
            chat_box
        )
    )

    send_button.pack(
        pady=5
    )

    return message_box, chat_box