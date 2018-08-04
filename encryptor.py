from Crypto.PublicKey import RSA
import base64
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from key import KeyGenerator

import filesystem
import constants

BLOCK_SIZE = 32

class FileEncryptor:
    def __init__(self, key=None):
        self.key = key

    def encrypt(self, plaintext, output):
        file = open(plaintext, 'rb')
        output_file = open(output, 'wb')
        iv = get_random_bytes(16)
        # print(iv)
        encryptor = AES.new(self.key, AES.MODE_CBC, iv)

        data = file.read()
        cipher_text = iv + encryptor.encrypt(pad(data, BLOCK_SIZE))
        # base64.b64encode(cipher_text)
        # print(base64.b64encode(cipher_text))
        output_file.write(base64.b64encode(cipher_text))
        file.close()
        output_file.close()

    def decrypt(self, ciphertext):
        file = open(ciphertext, 'rb')
        raw = file.read()

        raw = base64.b64decode(raw)
        # print(raw)
        iv = raw[:16]


        # iv = base64.b64decode(test)

        try:
            decryptor = AES.new(self.key, AES.MODE_CBC, iv)
            data = raw[16:]
            plaintext = decryptor.decrypt(data)
            # print(unpad(plaintext, BLOCK_SIZE))
            # output_file.write(unpad(plaintext, BLOCK_SIZE))
            return unpad(plaintext, BLOCK_SIZE)
        except ValueError:
            print('Something went wrong when loading your key.\n'
                  'Please ensure that your key file is valid')
            raise
        except:
            print('Oops! Something went wrong')

        file.close()



if __name__ == "__main__":
    print(constants.WELCOME_MESSAGE)
    key = None
    done = False
    while not done:
        choice = input('Enter your choice: ')
        if (choice =='y'):
            try:
                path = filesystem.selectFile()
                key_file = open(path, 'rb')
                key = key_file.read()
                done = True
            except FileNotFoundError:
                print('Key file was not found. Make sure you have the right path')
        if (choice == 'n'):
            generator = KeyGenerator()
            key = generator.saveKeyFile()
            done = True

    done = False
    print('Welcome to PyPass!')
    while not done:
        print('Type "d" to see your passwords\n'
              'Type "e" to encrypt your information.\n'
              'Type "k" to change your key\n'
              'Type done to quit')
        option = input('Enter a command: ')
        if (option == constants.DECRYPT_OPT):
            decryp = FileEncryptor(key)
            path = filesystem.selectFile()
            if (path != "()"):
                info_bytestring = decryp.decrypt(path)
                if info_bytestring:
                    print(info_bytestring.decode('utf-8'))
        if (option == constants.ENCRYPT_OPT):
            path = filesystem.selectFile()
            target = filesystem.selectDir()
            if path != "" and target != "()":
                encryp = FileEncryptor(key)
                encryp.encrypt(path, target + '/ciphertext.txt')
            else:
                print("Path or target not valid. Please try again.")
        if (option == constants.CHANGE_KEY_OPT):
            path = filesystem.selectFile()
            if path:
                key_file = open(path, 'rb')
                key = key_file.read()
                print("Succesfully swapped key!")
            else:
                print("Error when swapping key")
        if (option == "done"):
            done = True


