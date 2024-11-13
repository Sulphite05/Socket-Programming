import socket
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

SERVER_HOST = 'localhost'
SERVER_PORT = 12345
BUFFER_SIZE = 4096


class ServerGUI:
    def __init__(self, root):
        # Main application window
        self.root = root
        self.root.title("File Server")  # Set title of the window
        self.root.geometry("350x200")  # Set window dimensions
        self.root.configure(bg="#FFEBEE")  # Set background color

        self.file_label = tk.Label(root, text="No file selected", font=("Helvetica", 12), bg="#FFEBEE", fg="#333")
        self.file_label.pack(pady=10)

        self.select_button = tk.Button(root, text="Select File", command=self.select_file, font=("Helvetica", 12), width=15)
        self.select_button.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            self.file_label.config(text=file_path)

            threading.Thread(target=self.start_server, args=(file_path,)).start()

    def start_server(self, file_path):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVER_HOST, SERVER_PORT))

        server_socket.listen(1)
        print(f"[*] Server listening on {SERVER_HOST}:{SERVER_PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")

            threading.Thread(target=self.handle_client, args=(client_socket, file_path)).start()

    def handle_client(self, client_socket, file_path):
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()
                client_socket.sendall(file_data)
                print("[*] File sent successfully.")

                messagebox.showinfo("Success", "File sent successfully.")
        except FileNotFoundError:
            print("[!] File not found.")
            client_socket.sendall(b'File not found')
        finally:
            client_socket.close()


root = tk.Tk()
ServerGUI(root)
root.mainloop()
