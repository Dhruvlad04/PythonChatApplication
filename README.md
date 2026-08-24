# Python Chat Application

This is a small client/server chat program written in Python. I built it to practise TCP sockets, threads, and a Tkinter event loop.

## How to run it

Open two or more terminal windows in this folder.

1. Start the server:

   ```text
   python server.py
   ```

2. Start a client in another terminal:

   ```text
   python main.py
   ```

3. Start another client with the same command if messages need to be tested between two windows.

The server uses `127.0.0.1`, so the clients and server must be running on the same computer. The port is `5000` in both `server.py` and `main.py`.

## What I learned

A socket is the communication endpoint for a program. The server creates a TCP socket, binds it to an address, calls `listen()`, and then uses `accept()` to create a connection for each client. The client creates its own socket and calls `connect()`.

After a connection exists, both sides use `sendall()` to send bytes and `recv()` to read bytes. Messages are converted to bytes with `encode()` before sending and converted back to text with `decode()` after receiving. An empty result from `recv()` means the other side has disconnected.

`recv()` waits for data, so it cannot run in the Tkinter thread. The client starts a receiver thread for this blocking operation. Tkinter remains in charge of its own widgets and uses `root.after()` to check the receiver's message list every 100 milliseconds. A lock protects that list while the two threads use it.

The server has an accept thread because `accept()` also waits. Each connected client gets another thread, which means one quiet client does not stop other clients from sending messages.

## Debugging and changes

I started with a working single-client prototype and then tested the parts that were easiest to get wrong:

- When no server was running, the client raised `ConnectionRefusedError`. I added a message explaining which program to start first.
- Putting `recv()` in the GUI code made the window liable to freeze while waiting. I moved receiving into a thread and used `after()` for GUI updates.
- The receiver and GUI could access the message list at the same time. I added a lock and made `get_messages()` copy and clear the list as one operation.
- A disconnected client could change the server's client list during a broadcast. I made a snapshot of the list while holding a lock.
- I replaced broad exception handling with `OSError`, which is the type expected for socket failures, so programming mistakes are not silently hidden.

The detailed code comments are next to the socket and threading operations in `client.py`, `server.py`, and `main.py`.

## Checks

The Python files compile with:

```text
python -m py_compile client.py server.py layout.py main.py
```

A local socket test also confirmed that a client can connect, send a message, receive an echo on its background thread, and close cleanly.
