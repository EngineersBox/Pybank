from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib

class keyGen:

    def newKey():
        key = Fernet.generate_key()
        return Fernet(key)

    def newKeyPasswd(password):
        password_provided = password # This is input in the form of a string
        password = password_provided.encode() # Convert to type bytes
        salt = os.urandom(16) # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
        return key

class msgEnc:

    def encMsg(key, message):
        return key.encrypt(str(message).encode("utf-8"))

    def decMsg(key, token):
        return key.decrypt(token)

class fileEnc:

    def storeKey(filename, key):
        file = open(filename, 'wb')
        file.write(key)
        file.close()

    def readKey(filename):
        file = open(filename, 'rb')
        key = file.read(key) # The key will be type bytes
        file.close()
        return key

    def encFile(inFile, outFile, key=keyGen.newKey()):
        storeKey("key.key", key)
        input_file = inFile #.txt
        output_file = outFile #.encrypted

        with open(input_file, 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)

        with open(output_file, 'wb') as f:
            f.write(encrypted)

    def decFile(inFile, outFile):
        key = readKey("key.key")
        input_file = inFile #.encrypted
        output_file = outFile #.txt

        with open(input_file, 'rb') as f:
            data = f.read()

        fernet = Fernet(key)
        encrypted = fernet.decrypt(data)

        with open(output_file, 'wb') as f:
            f.write(encrypted)
