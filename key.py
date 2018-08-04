import tkinter as tk
from tkinter import filedialog
from Crypto.Random import get_random_bytes

class KeyGenerator:
    def saveKeyFile(self):
        root = tk.Tk()
        file = tk.filedialog.asksaveasfile(mode='wb', defaultextension=".txt")
        key = get_random_bytes(16)
        file.write(key)
        root.destroy()
        return key