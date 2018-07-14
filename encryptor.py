from Crypto.PublicKey import RSA
import base64
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

import tkinter as tk
from tkinter import StringVar
from tkinter import filedialog
from tkinter import font  as tkfont
import constants

BLOCK_SIZE = 32

class FileEncryptor:
    def __init__(self, key=None):
        self.key = key

    def encrypt(self, plaintext, output):
        file = open(plaintext, 'rb')
        output_file = open(output, 'wb')
        iv = get_random_bytes(16)
        encryptor = AES.new(self.key, AES.MODE_CBC, iv)

        output_file.write(base64.b64encode(iv))
        data = file.read()
        cipher_text = encryptor.encrypt(pad(data, BLOCK_SIZE))
        # base64.b64encode(cipher_text)
        output_file.write(base64.b64encode(pad(cipher_text, BLOCK_SIZE)))
        file.close()
        output_file.close()

    def decrypt(self, ciphertext):
        file = open(ciphertext, 'rb')
        iv = file.read(16)
        # print(test)
        # iv = base64.b64decode(test)
        # print(iv)


        try:
            decryptor = AES.new(self.key, AES.MODE_CBC, iv)
            data = unpad(base64.b64decode(file.read()), BLOCK_SIZE)
            plaintext = decryptor.decrypt(data)
            # print(unpad(plaintext, BLOCK_SIZE))
            # output_file.write(unpad(plaintext, BLOCK_SIZE))
            return unpad(plaintext, BLOCK_SIZE)
        except ValueError:
            print('Something went wrong when loading your key.\n'
                  'Please ensure that your key file is valid')
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

def saveKeyFile():
    root = tk.Tk()
    file = tk.filedialog.asksaveasfile(mode='wb', defaultextension=".txt")
    key = get_random_bytes(16)
    file.write(key)
    root.destroy()
    return key

if __name__ == "__main__":
    print(constants.WELCOME_MESSAGE)
    key = None
    done = False
    while not done:
        choice = input('Enter your choice: ')
        if (choice =='y'):
            try:
                path = selectFile()
                key_file = open(path, 'rb')
                key = key_file.read()
                done = True
            except FileNotFoundError:
                print('Key file was not found. Make sure you have the right path')
        if (choice == 'n'):
            key = saveKeyFile()
            done = True

    done = False
    print('Welcome to PyPass!')
    while not done:
        print('Type "d" to see your passwords\n'
              'Type "e" to encrypt your information.\n'
              'Type done to quit')
        option = input('Enter a command: ')
        if (option == constants.DECRYPT_OPT):
            decryp = FileEncryptor(key)
            path = selectFile()
            info_bytestring = decryp.decrypt(path)
            if info_bytestring:
                print(info_bytestring.decode('utf-8'))
        if (option == constants.ENCRYPT_OPT):
            path = selectFile()
            target = selectDir()
            if path != "" and target != "()":
                encryp = FileEncryptor(key)
                encryp.encrypt(path, target + '/ciphertext.txt')
            else:
                print("Path or target not valid. Please try again.")
        if (option == "done"):
            done = True


