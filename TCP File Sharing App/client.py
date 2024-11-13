import socket
from tkinter import Tk, Button, Label, filedialog, messagebox


SERVER_HOST = 'localhost'
SERVER_PORT = 12345
BUFFER_SIZE = 4096


class ClientGUI:
    def __init__(self, root):
        # Main app window
        self.root = root
        self.root.title("File Receiver")
        self.root.geometry("350x200")
        self.root.configure(bg="#E8F6EF")

        self.file_label = Label(root, text="No file received", font=("Helvetica", 12), bg="#E8F6EF", fg="#333")
        self.file_label.pack(pady=10)

        self.receive_button = Button(root, text="Receive File", command=self.receive_file, font=("Helvetica", 12),
                                      width=15)
        self.receive_button.pack(pady=10)

    def receive_file(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client_socket.connect((SERVER_HOST, SERVER_PORT))

            file_name = filedialog.asksaveasfilename(defaultextension=".*")

            if file_name:
                with open(file_name, 'wb') as file:
                    while True:
                        # data in chunks from the server
                        file_data = client_socket.recv(BUFFER_SIZE)

                        if not file_data:
                            break
                        file.write(file_data)

                self.file_label.config(text=f"File saved as: {file_name}")
                print("[*] File received and saved.")
                messagebox.showinfo("Success", "File received and saved successfully.")
            else:
                print("[!] No file name provided.")

        except Exception as e:
            print(f"[!] Error: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

        finally:
            client_socket.close()


root = Tk()
ClientGUI(root)
root.mainloop()
