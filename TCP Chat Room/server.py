import socket
import threading


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_Stream for TCP
server.bind(("localhost", 5555))
server.listen()

clients = dict()
print("Server is listening...")


def broadcast(message, sender=None):
    """Sends a message to all connected clients except the sender."""
    for client in clients:
        if client != sender:
            client.send(message)


def handle(client):
    """Handles messages from a specific client."""
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            nickname = clients.pop(client, None)
            broadcast(f"{nickname} left the chat!".encode())
            client.close()
            break


def receive():
    """Accepts new clients and starts a thread for each one."""
    while True:
        client, _ = server.accept()     # server accepts connection here showing TCP conn
        client.send("NICK".encode())
        nickname = client.recv(1024).decode()

        clients[client] = nickname
        broadcast(f"{nickname} joined the chat!".encode())
        print(f"{nickname} connected!")

        threading.Thread(target=handle, args=(client,)).start()


# Start receiving clients
receive()
