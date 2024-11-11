import socket
import threading
import random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000, 9000)))  # binding to a random port
name = input("Nickname: ")


def receive():
    """Receives messages from the server."""
    while True:
        try:
            message, _ = client.recvfrom(1024)  # receive messages from server
            print(message.decode())
        except Exception as e:
            print(f"Error receiving message: {e}")


t = threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG:{name}".encode(), ("localhost", 9998))

while True:
    message = input()
    client.sendto(f"{name}: {message}".encode(), ("localhost", 9998))
