import tkinter as tk

from client import ChatClient
from layout import create_layout


HOST = "127.0.0.1"
PORT = 5000


# Connect the GUI client to the server
try:

    client = ChatClient(HOST, PORT)

except ConnectionRefusedError:

    print("Please start server.py first.")
    exit()


# Send a message from the GUI
def send_message(message_box, chat_box):

    message = message_box.get()

    if message == "":
        return

    # Send the message using the client socket
    client.send_message(message)

    # Display the message in the chat box
    chat_box.insert(
        tk.END,
        "You: " + message + "\n"
    )

    message_box.delete(
        0,
        tk.END
    )


# Check whether the server sent a message
def check_messages():

    messages = client.get_messages()

    for message in messages:

        # Display the received message
        chat_box.insert(
            tk.END,
            message + "\n"
        )

    if client.running:

        # Check again after 100 milliseconds
        root.after(
            100,
            check_messages
        )


# Close the application
def close_application():

    try:
        client.send_message("exit")
    except OSError:
        pass

    client.close()

    root.destroy()


# Create the main Tkinter window
root = tk.Tk()

# Create the chat interface
message_box, chat_box = create_layout(
    root,
    send_message
)

# Start receiving messages from the server
client.start_receiving()

# Start checking for received messages
root.after(
    100,
    check_messages
)

# Run close_application when X is clicked
root.protocol(
    "WM_DELETE_WINDOW",
    close_application
)

# Keep the GUI running
root.mainloop()