import random
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
import base64
import os
from cryptography.fernet import Fernet

def get_random_number():
    projectId = random.randint(100000,999999)
    return projectId

def generate_secret_key():
    return os.urandom(32)

class EncryptionHelper:
    # Ensure the key is 16, 24, or 32 bytes long
    SECRET_KEY = generate_secret_key()
    # BLOCK_SIZE = AES.block_size

    @staticmethod
    def encrypt(text):
        cipher = AES.new(EncryptionHelper.SECRET_KEY, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), EncryptionHelper.BLOCK_SIZE))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        return iv + ct

    @staticmethod
    def decrypt(iv_ct):
        try:
            iv = base64.b64decode(iv_ct[:24])
            ct = base64.b64decode(iv_ct[24:])
            cipher = AES.new(EncryptionHelper.SECRET_KEY, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), EncryptionHelper.BLOCK_SIZE)
            return pt.decode('utf-8')
        except Exception as e:
            print(f"Decryption error: {e}")
            return None

key = Fernet.generate_key()
fernet = Fernet(key)

def encrypt_id(id):
    """Encrypts an ID."""
    # Ensure the ID is a string
    id_str = str(id)
    # Encrypt the ID
    enc_id = fernet.encrypt(id_str.encode())
    return enc_id.decode()

def decrypt_id(enc_id):
    """Decrypts an ID."""
    # Decrypt the ID
    dec_id = fernet.decrypt(enc_id.encode())
    return int(dec_id.decode())