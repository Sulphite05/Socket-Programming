import socket
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

# Define server IP address and port
SERVER_HOST = 'localhost'  # Localhost IP
SERVER_PORT = 12345  # Port to listen for client connection
BUFFER_SIZE = 4096  # Size of the buffer for data packets


class ServerGUI:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root
        self.root.title("File Server")  # Set title of the window
        self.root.geometry("350x200")  # Set window dimensions
        self.root.configure(bg="#FFEBEE")  # Set background color

        # Label to show the selected file path
        self.file_label = tk.Label(root, text="No file selected", font=("Helvetica", 12), bg="#FFEBEE", fg="#333")
        self.file_label.pack(pady=10)

        # Button to open file dialog and select file
        self.select_button = tk.Button(root, text="Select File", command=self.select_file, font=("Helvetica", 12), width=15)
        self.select_button.pack(pady=10)

    def select_file(self):
        # Prompt the user to select a file to send
        file_path = filedialog.askopenfilename()

        if file_path:
            # Update UI to display the selected file path
            self.file_label.config(text=file_path)

            # Start the server in a new thread to handle file sending
            threading.Thread(target=self.start_server, args=(file_path,)).start()

    def start_server(self, file_path):
        # Create a socket for the server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the specified host and port
        server_socket.bind((SERVER_HOST, SERVER_PORT))

        # Start listening for incoming client connections
        server_socket.listen(1)
        print(f"[*] Server listening on {SERVER_HOST}:{SERVER_PORT}")

        while True:
            # Accept a connection from a client
            client_socket, client_address = server_socket.accept()
            print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")

            # Start a new thread to handle the connected client
            threading.Thread(target=self.handle_client, args=(client_socket, file_path)).start()

    def handle_client(self, client_socket, file_path):
        try:
            # Open the selected file in binary read mode
            with open(file_path, 'rb') as file:
                # Read and send the file content to the client
                file_data = file.read()
                client_socket.sendall(file_data)
                print("[*] File sent successfully.")

                # Display success message on the server side
                messagebox.showinfo("Success", "File sent successfully.")
        except FileNotFoundError:
            # Handle the case where the file is not found
            print("[!] File not found.")
            client_socket.sendall(b'File not found')
        finally:
            # Close the client socket connection
            client_socket.close()


def main():
    # Initialize Tkinter and create the server GUI
    root = tk.Tk()
    server_gui = ServerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()