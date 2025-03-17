from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP

class RSACipher:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        key = RSA.generate(2048)
        self.private_key = key
        self.public_key = key.publickey()

   
    def load_keys(self):
        if self.private_key is None or self.public_key is None:
            raise ValueError("Keys not generated")
        return self.private_key, self.public_key
    
    def encrypt(self, message, key):
        cipher = PKCS1_OAEP.new(key)
        return cipher.encrypt(message.encode())
    

    def decrypt(self, cipher_text, key):
        cipher = PKCS1_OAEP.new(key)
        return cipher.decrypt(cipher_text).decode()
    
    def sign(self, message,key):
        hash = SHA256.new(message.encode())
        return PKCS1_v1_5.new(key).sign(hash)
    
    def verify(self, message, signature, key):
        hash = SHA256.new(message.encode())
        try:
            PKCS1_v1_5.new(key).verify(hash, signature)
            return True
        except (ValueError, TypeError):
            return False
        