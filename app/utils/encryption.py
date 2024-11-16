from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv('FERNET_KEY')

class EncryptionUtils:
    key = key.encode()

    def encrypt(text: str):
        fernet = Fernet(EncryptionUtils.key)
        return fernet.encrypt(text.encode()).decode()

    def decrypt(token: str):
        fernet = Fernet(EncryptionUtils.key)
        return fernet.decrypt(token.encode()).decode()