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


if __name__ == "__main__":
    print('Welcome to the FileEncryptor!\nIf you have a key file, type y\n If you don\'t, type n\n to quit, type q')

    done = False
    while not done:
        choice = input('Enter your choice: ')
        if (choice == 'y'):
            key_path = input('Enter the path to the key file: ')
        # try:
        #     key_file = open('key.txt', 'rb')
        #     print('Found key file')
        #     test = FileEncryptor(key_file.read())
        # except FileNotFoundError:
        #     print('key file not found. Generating')
        #     test = FileEncryptor()
        #     output_key = open('key.txt', 'wb')
        #     output_key.write(test.key)


    done = False
    while not done:
        print('Welcome to the FileEncryptor!\nType "e" to encrypt a file\nType "d" to decrypt a file.\nType done to quit')
        option = input('Enter a command: ')
        if (option == 'e'):
            test.encrypt('plaintext.txt', 'ciphertext.txt')
        if (option == 'd'):
            test.decrypt('ciphertext.txt', 'decrypted.txt')
        if (option == "done"):
            done = True
    BLOCK_SIZE = 32
    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    encryption_suite = AES.new(key, AES.MODE_CBC, iv)
    file = open('plaintext.txt', 'rb')
    data = file.read()
    cipher_text = encryption_suite.encrypt(pad(data, BLOCK_SIZE))

