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

    def decrypt(self, ciphertext):
        print(self.key)
        file = open(ciphertext, 'rb')
        iv = file.read(16)
        # print(test)
        # iv = base64.b64decode(test)
        # print(iv)
        decryptor = AES.new(self.key, AES.MODE_CBC, iv)

        try:
            data = unpad(base64.b64decode(file.read()), BLOCK_SIZE)
            plaintext = decryptor.decrypt(data)
            # print(unpad(plaintext, BLOCK_SIZE))
            # output_file.write(unpad(plaintext, BLOCK_SIZE))
            return unpad(plaintext, BLOCK_SIZE)
        except:
            print('Oops! Something went wrong')

        file.close()


def generateKeyFile(path):
    try:
        key = open(path + '/key.txt', 'wb')
        key.write(get_random_bytes(16))
        print("Created your new key! Make sure you don't share the key with ANYONE!")
    except:
        print('Something went wrong!')
        exit(1)

if __name__ == "__main__":
    print('Welcome to the FileEncryptor!\nIf you have a key file, type y\n If you don\'t, type n\n to quit, type q')
    key = None
    done = False
    while not done:
        choice = input('Enter your choice: ')
        if (choice =='y'):
            try:
                key_file = open('key.txt', 'rb')
                key = key_file.read()
                done = True
            except FileNotFoundError:
                print('Key file was not found. Make sure you have the right path')
        if (choice == 'n'):
            key_path = input('Enter the path to the key file: ')
            generateKeyFile(key_path)
            done = True

    done = False
    while not done:
        print('Welcome to the FileEncryptor!\nType "d" to see your information\nType "e" to encrypt your information.\nType done to quit')
        option = input('Enter a command: ')
        if (option == 'd'):
            decryp = FileEncryptor(key)
            print(decryp.decrypt('test/ciphertext.txt'))
        if (option == 'e'):
            encryp = FileEncryptor(key)
            encryp.encrypt('test/plaintext.txt', 'test/ciphertext.txt')
        if (option == "done"):
            done = True
    # BLOCK_SIZE = 32
    # key = get_random_bytes(16)
    # iv = get_random_bytes(16)
    # encryption_suite = AES.new(key, AES.MODE_CBC, iv)
    # file = open('plaintext.txt', 'rb')
    # data = file.read()
    # cipher_text = encryption_suite.encrypt(pad(data, BLOCK_SIZE))

