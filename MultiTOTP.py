import pyotp
import tkinter as tk
from tkinter import ttk
import pyperclip
import csv
import sys
import os
import logging

def read_secrets(file_path):
    try:
        #make sure file exists, if not create it
        if not os.path.isfile(file_path):
            # Ensure the directory exists
            os.makedirs('C:\\ProgramData\\MFATool\\', exist_ok=True)
            logging.debug(f"File does not exist, checking if path exists")
            # Create the empty CSV file
            open('C:\\ProgramData\\MFATool\\secrets.csv', 'w').close()
            logging.debug(f"Secret File Created")

        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            return [(row[0].strip(), row[1].strip()) for row in reader]
    except FileNotFoundError:
        logging.debug(f"Secrets file doesn't exist")
        sys.exit(1)
    except Exception as e:
        logging.debug(f"An error occurred: {e}")
        sys.exit(1)

def write_secret(file_path, name, secret):
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, secret])
        logging.debug(f"New Secret Added, Name: {name}")

class AddEntryWindow:
    def __init__(self, parent, callback):
        self.top = tk.Toplevel(parent)
        self.top.title("Add New Entry")
        self.callback = callback

        # Name input
        ttk.Label(self.top, text="Name:", font=('Helvetica', 12)).pack(pady=(10, 0))
        self.name_entry = ttk.Entry(self.top, width=50)
        self.name_entry.pack()

        # Secret input
        ttk.Label(self.top, text="Secret:", font=('Helvetica', 12)).pack(pady=(10, 0))
        self.secret_entry = ttk.Entry(self.top, width=50)
        self.secret_entry.pack()

        # Add button
        add_button = ttk.Button(self.top, text="Add", command=self.add_entry)
        add_button.pack(pady=20)

    def add_entry(self):
        name = self.name_entry.get()
        secret = self.secret_entry.get()
        if name and secret:
            self.callback(name, secret)
            self.top.destroy()

class TOTPGeneratorApp:
    def __init__(self, master, entries):
        self.master = master
        self.file_path = 'C:\\ProgramData\\MFATool\\secrets.csv'
        logging.debug(f'TOPGenerator Entries: {entries}')
        self.entries = entries
        #master.title("MFA Code Generator")

        # Main Frame for TOTPs
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(padx=10, pady=10, fill='x', expand=True)

        self.empty_label = ttk.Label(self.main_frame, text="No MFA Codes Defined", font=('Helvetica', 14))

        self.widgets = []
        self.build_totp_widgets()

        # Button to open add entry window
        #removing this for the VB365 build - No need for end user modification here.
        #add_button = ttk.Button(master, text="Add New Entry", command=self.open_add_entry_window)
        #add_button.pack(pady=10)

    def build_totp_widgets(self):

        for widget in self.widgets:
            widget[0].destroy()
        self.widgets = []

        if not self.entries:
            self.empty_label.pack(padx=10, pady=20)
            return
        else:
            self.empty_label.pack_forget()
            for name, secret in self.entries:
                frame = ttk.Frame(self.main_frame)
                frame.pack(padx=10, pady=5, fill='x', expand=True)

                label = ttk.Label(frame, text=f"{name} MFA Code:", font=('Helvetica', 14))
                totp_display = ttk.Label(frame, text="", font=('Helvetica', 14))
                copy_button = ttk.Button(frame, text="Copy", command=lambda totp_display=totp_display: self.copy_to_clipboard(totp_display))
                
                label.pack(side=tk.LEFT, padx=10)
                copy_button.pack(side=tk.RIGHT, padx=10)
                totp_display.pack(side=tk.RIGHT, padx=10)

                self.widgets.append((frame, totp_display, pyotp.TOTP(secret)))

        self.update_totps()


    def update_totps(self):
        #logging.debug(f'Updating TOTPs')
        for _, totp_display, totp in self.widgets:
            totp_display.config(text=totp.now())
        
        self.master.after(1000, self.update_totps)

    def copy_to_clipboard(self, totp_display):
        pyperclip.copy(totp_display['text'])

    def open_add_entry_window(self):
        AddEntryWindow(self.master, self.add_secret)

    def add_secret(self, name, secret):
        write_secret(self.file_path, name, secret)
        self.entries.append((name, secret))
        self.build_totp_widgets()

if __name__ == "__main__":


    base_path = 'C:\\ProgramData\\MFATool\\'

    logging_path = os.path.join(base_path, 'logs\\')
    os.makedirs(f'{logging_path}', exist_ok=True)
    logging.basicConfig(filename=f'{logging_path}\\mfa-app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



    secrets_file_path = os.path.join(base_path, 'C:\\ProgramData\\MFATool\\', 'secrets.csv')
    entries = read_secrets(secrets_file_path)
    root = tk.Tk()
    root.title("MFA Code Generator")

    app = TOTPGeneratorApp(root, entries)
    root.mainloop()
