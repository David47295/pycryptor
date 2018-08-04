import tkinter as tk
from tkinter import filedialog

def selectFile():
    root = tk.Tk()
    path = tk.filedialog.askopenfilename()
    root.destroy()
    return path

def selectDir():
    root = tk.Tk()
    path = tk.filedialog.askdirectory()
    root.destroy()
    return path