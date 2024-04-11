import pyotp
import tkinter as tk
from tkinter import ttk
import pyperclip
import csv

def read_secrets(file_path):
    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            return [(row[0].strip(), row[1].strip()) for row in reader]
    except FileNotFoundError:
        print("CSV file not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

class TOTPGeneratorApp:
    def __init__(self, master, entries):
        self.master = master
        master.title("MFA Codes")

        self.entries = entries
        self.widgets = []

        for name, secret in entries:
            frame = ttk.Frame(master)
            frame.pack(padx=10, pady=10, fill='x')

            label = ttk.Label(frame, text=f"{name} TOTP:", font=('Helvetica', 14))
            label.pack(side=tk.LEFT, padx=10)

            totp_display = ttk.Label(frame, text="", font=('Helvetica', 14))
            totp_display.pack(side=tk.LEFT, padx=10)
            
            copy_button = ttk.Button(frame, text="Copy", command=lambda totp=totp_display: self.copy_to_clipboard(totp))
            copy_button.pack(side=tk.RIGHT, padx=10)

            self.widgets.append((totp_display, pyotp.TOTP(secret)))

        self.update_totps()

    def update_totps(self):
        for totp_display, totp in self.widgets:
            totp_display.config(text=totp.now())
        
        self.master.after(1000, self.update_totps)

    def copy_to_clipboard(self, totp_display):
        pyperclip.copy(totp_display['text'])

if __name__ == "__main__":
    secrets_file_path = 'C:\\temp\\secrets.csv'
    entries = read_secrets(secrets_file_path)
    root = tk.Tk()
    app = TOTPGeneratorApp(root, entries)
    root.mainloop()
