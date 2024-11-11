import socket
import threading

messages = []
clients = set()  # for faster client address management
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9998))


def receive():
    """Receives messages from any client without setting up connection."""
    while True:
        try:
            message, address = server.recvfrom(1024)
            messages.append((message, address))
        except Exception as e:
            print(f"Error receiving message: {e}")


def broadcast():
    """Sends a message to all connected clients."""
    while True:
        if messages:
            message, address = messages.pop(0)
            print(message.decode())
            if address not in clients:
                clients.add(address)
            for client in list(clients):
                try:
                    dec_mess = message.decode()
                    if dec_mess.startswith("SIGNUP_TAG:"):
                        name = dec_mess[11:]  # extracts the name after SIGNUP_TAG
                        server.sendto(f"{name} joined!".encode(), client)
                    else:   # broadcasts message to all clients
                        server.sendto(message, client)
                except Exception as e:
                    print(f"Error sending message to {client}: {e}")
                    clients.remove(client)


recv_thread = threading.Thread(target=receive)
recv_thread.start()
broadcast_thread = threading.Thread(target=broadcast)
broadcast_thread .start()
