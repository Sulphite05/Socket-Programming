import socket
import threading


nickname = input("Choose a nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5555))


def receive():
    """Receives messages from the server."""
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "NICK":
                client.send(nickname.encode())
            else:
                print(message)
        except:
            print("Disconnected from the server!")
            client.close()
            break


def write():
    """Takes input from the user and sends it to the server."""
    while True:
        message = f"{nickname}: {input()}"
        client.send(message.encode())


# Start threads for receiving and writing messages
threading.Thread(target=receive).start()
threading.Thread(target=write).start()
