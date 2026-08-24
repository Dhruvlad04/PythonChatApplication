import tkinter as tk


def create_layout(root, send_function):

    root.title("Python Chat Application")
    root.geometry("600x500")

    # Chat display area
    chat_box = tk.Text(
        root,
        width=65,
        height=20
    )

    chat_box.pack(pady=10)

    # Message input
    message_box = tk.Entry(
        root,
        width=45
    )

    message_box.pack(pady=5)

    # Send button
    send_button = tk.Button(
        root,
        text="Send",
        width=10,
        command=lambda: send_function(
            message_box,
            chat_box
        )
    )

    send_button.pack(pady=5)

    return message_box, chat_box