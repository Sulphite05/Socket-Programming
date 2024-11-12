import socket
from tkinter import Tk, Button, Label, filedialog, messagebox
import tkinter as tk

# Define server IP address and port
SERVER_HOST = 'localhost'  # Localhost IP
SERVER_PORT = 12345  # Port to listen for the connection
BUFFER_SIZE = 4096  # Size of the buffer for data packets


class ClientGUI:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root
        self.root.title("File Receiver")  # Set title of the window
        self.root.geometry("350x200")  # Set window dimensions
        self.root.configure(bg="#E8F6EF")  # Set background color

        # Label to show the status of file reception
        self.file_label = Label(root, text="No file received", font=("Helvetica", 12), bg="#E8F6EF", fg="#333")
        self.file_label.pack(pady=10)

        # Button to trigger file reception from server
        self.receive_button = Button(root, text="Receive File", command=self.receive_file, font=("Helvetica", 12),
                                      width=15)
        self.receive_button.pack(pady=10)

    def receive_file(self):
        # Create a socket for the client to connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Attempt to connect to the server
            client_socket.connect((SERVER_HOST, SERVER_PORT))

            # Prompt the user to select a location to save the received file
            file_name = filedialog.asksaveasfilename(defaultextension=".*")

            # Only proceed if a file name is provided
            if file_name:
                # Open the specified file path for writing the received data
                with open(file_name, 'wb') as file:
                    while True:
                        # Receive data in chunks from the server
                        file_data = client_socket.recv(BUFFER_SIZE)

                        # Stop receiving if no more data is sent
                        if not file_data:
                            break
                        # Write the received chunk to the file
                        file.write(file_data)

                # Update UI to show success message
                self.file_label.config(text=f"File saved as: {file_name}")
                print("[*] File received and saved.")
                messagebox.showinfo("Success", "File received and saved successfully.")
            else:
                print("[!] No file name provided.")

        except Exception as e:
            # Show error if something goes wrong
            print(f"[!] Error: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

        finally:
            # Close the client socket connection
            client_socket.close()


def main():
    # Initialize Tkinter and create the client GUI
    root = Tk()
    client_gui = ClientGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()