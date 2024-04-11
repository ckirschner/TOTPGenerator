import pyotp
import tkinter as tk
from tkinter import ttk
import pyperclip

def read_secret_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()  # Read the secret key and strip any extraneous whitespace
    except FileNotFoundError:
        print("Secret file not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

class TOTPGeneratorApp:
    def __init__(self, master, secret):
        self.master = master
        master.title("MFA Codes")

        # Create a TOTP object
        self.totp = pyotp.TOTP(secret)

        # Setup the UI
        self.label = ttk.Label(master, text="Current TOTP:", font=('Helvetica', 14))
        self.label.pack(pady=20)

        self.totp_display = ttk.Label(master, text="", font=('Helvetica', 24))
        self.totp_display.pack(pady=10)

        self.copy_button = ttk.Button(master, text="Copy", command=self.copy_to_clipboard)
        self.copy_button.pack(pady=5)

        self.update_totp()

    def update_totp(self):
        # Update the displayed TOTP
        current_totp = self.totp.now()
        self.totp_display.config(text=current_totp)
        
        # Schedule an update every second
        self.master.after(1000, self.update_totp)

    def copy_to_clipboard(self):
        # Copy current TOTP to clipboard
        pyperclip.copy(self.totp_display['text'])

if __name__ == "__main__":
    secret_file_path = 'C:\\temp\\secret.txt'
    currentsecret = read_secret_file(secret_file_path)  # Read the secret key from the file
    root = tk.Tk()
    app = TOTPGeneratorApp(root, currentsecret)  # Replace YOUR_SECRET_KEY with your actual key
    root.mainloop()
