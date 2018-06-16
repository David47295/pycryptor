from Crypto.PublicKey import RSA
import base64
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

import tkinter as tk
from tkinter import StringVar
from tkinter import filedialog
from tkinter import font  as tkfont

BLOCK_SIZE = 32

class FileEncryptor:
    def __init__(self, key=None):
        if (key == None):
            # self.key = get_random_bytes(16)
            self.key = None
        else:
            self.key = key

    def encrypt(self, plaintext, output):
        file = open(plaintext, 'rb')
        output_file = open(output, 'wb')
        iv = get_random_bytes(16)
        encryptor = AES.new(self.key, AES.MODE_CBC, iv)

        # output_file.write(base64.b64encode(iv))
        output_file.write(iv)
        data = file.read()
        cipher_text = encryptor.encrypt(pad(data, BLOCK_SIZE))
        # base64.b64encode(cipher_text)
        output_file.write(base64.b64encode(pad(cipher_text, BLOCK_SIZE)))
        file.close()
        output_file.close()

    def decrypt(self, ciphertext, output):
        file = open(ciphertext, 'rb')
        output_file = open(output, 'wb')
        iv = file.read(16)
        # print(test)
        # iv = base64.b64decode(test)
        # print(iv)
        decryptor = AES.new(self.key, AES.MODE_CBC, iv)

        try:
            data = unpad(base64.b64decode(file.read()), BLOCK_SIZE)
            plaintext = decryptor.decrypt(data)
            # print(unpad(plaintext, BLOCK_SIZE))
            output_file.write(unpad(plaintext, BLOCK_SIZE))
        except:
            print('Oops! Something went wrong')

        file.close()
        output_file.close()

class FileEncrypApp(tk.Tk):
    _encryptor = None
    _root = None
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self._encryptor = FileEncryptor()

        self._root = tk.Frame(self)
        self._root.pack(side="top", fill="both", expand=True)
        self._root.grid_rowconfigure(0, weight=1)
        self._root.grid_columnconfigure(0, weight=1)

        page = HomePage(parent=self._root, controller=self)

        page.grid(row=0, column=0, sticky="nsew")
        page.tkraise()

    def goToPage(self, page):
        if (page == 'NEW_KEY'):
            frame = SaveNewKeyPage(parent=self._root, controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()

    def setEncryptorKey(self, path):
        key_file = open(path, 'rb')
        self._encryptor.key = key_file.read()

class HomePage(tk.Frame):
    _key_path = None
    _controller = None
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self._key_path = StringVar(self)
        self._controller = controller

        tk.Label(self, text="This is the start page").grid(row=0)

        tk.Button(self, text="Select key file", command=self.setKeyPath).grid(row=1)
        tk.Label(self, textvariable=self._key_path).grid(row=1, column=1)

        tk.Button(self, text="Generate new key file", command=lambda: self._controller.goToPage('NEW_KEY')).grid(row=2)

        next_btn = tk.Button(self, text="Next", state=tk.DISABLED, command=self.test)
        next_btn.grid(row=3)

    def setKeyPath(self):
        self._key_path.set("Key Path: " + filedialog.askopenfilename())

    def test(self):
        return True
        # print(self._key_path)

class SaveNewKeyPage(tk.Frame):
    _key_path = None
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is the new key page").grid(row=0)
        # label.pack()

# class SampleApp(tk.Tk):
#
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#
#         self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
#
#         # the container is where we'll stack a bunch of frames
#         # on top of each other, then the one we want visible
#         # will be raised above the others
#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand=True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)
#
#         self.frames = {}
#         # for F in (StartPage):
#         page_name = StartPage.__name__
#         frame = StartPage(parent=container, controller=self)
#         self.frames[page_name] = frame
#
#         # put all of the pages in the same location;
#         # the one on the top of the stacking order
#         # will be the one that is visible.
#         frame.grid(row=0, column=0, sticky="nsew")
#
#         self.show_frame("StartPage")
#
#     def show_frame(self, page_name):
#         '''Show a frame for the given page name'''
#         frame = self.frames[page_name]
#         frame.tkraise()
#
# class StartPage(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         label = tk.Label(self, text="This is the start page", font=controller.title_font)
#         label.pack(side="top", fill="x", pady=10)
#
#         button1 = tk.Button(self, text="Go to Page One",
#                             command=lambda: controller.show_frame("PageOne"))
#         button2 = tk.Button(self, text="Go to Page Two",
#                             command=lambda: controller.show_frame("PageTwo"))
#         button1.pack()
#         button2.pack()


if __name__ == "__main__":
    app = FileEncrypApp()
    app.mainloop()
    # root = tk.Tk()
    # frame = tk.Frame(root)
    # frame.pack()
    #
    # label = tk.Label(root, text="Welcome to the FileEncryptor")
    # label.pack()
    #
    # button = tk.Button(frame,
    #           text='Select Key File',
    #           command=lambda: setKeyPath(root))
    # button.pack()
    # button1 = tk.Button(frame,
    #                    text='PRint',
    #                    command=lambda: getKey(root))
    # button.pack()
    # button1.pack()
    # root.mainloop()

    # print('Welcome to the FileEncryptor!\nIf you have a key file, type y\n If you don\'t, type n\n to quit, type q')

    # done = False
    # while not done:
    #     choice = input('Enter your choice: ')
    #     if (choice == 'y'):
    #         key_path = input('Enter the path to the key file: ')
    #     if (choice == )
    #     # try:
    #     #     key_file = open('key.txt', 'rb')
    #     #     print('Found key file')
    #     #     test = FileEncryptor(key_file.read())
    #     # except FileNotFoundError:
    #     #     print('key file not found. Generating')
    #     #     test = FileEncryptor()
    #     #     output_key = open('key.txt', 'wb')
    #     #     output_key.write(test.key)
    #
    #
    # done = False
    # while not done:
    #     print('Welcome to the FileEncryptor!\nType "e" to encrypt a file\nType "d" to decrypt a file.\nType done to quit')
    #     option = input('Enter a command: ')
    #     if (option == 'e'):
    #         test.encrypt('plaintext.txt', 'ciphertext.txt')
    #     if (option == 'd'):
    #         test.decrypt('ciphertext.txt', 'decrypted.txt')
    #     if (option == "done"):
    #         done = True
    # BLOCK_SIZE = 32
    # key = get_random_bytes(16)
    # iv = get_random_bytes(16)
    # encryption_suite = AES.new(key, AES.MODE_CBC, iv)
    # file = open('plaintext.txt', 'rb')
    # data = file.read()
    # cipher_text = encryption_suite.encrypt(pad(data, BLOCK_SIZE))

