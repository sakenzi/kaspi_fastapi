from cryptography.fernet import Fernet
import os


def decrypt_password(encrypted_password: str) -> str:
    secret_key = os.environ.get("KASPI_SECRET_KEY")
    if not secret_key:
        raise Exception("Missing decryption key")
    fernet = Fernet(secret_key.encode())
    return fernet.decrypt(encrypted_password.encode()).decode()
