import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet


def get_prompt():
    password = os.getenv("PROMPT_PASSWORD")
    if password:
        with open("prompt.salt", "rb") as fh:
            salt = fh.read()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=390_000, )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        f = Fernet(key)
        with open("prompt.enc", "rb") as fh:
            enc = fh.read()
        return f.decrypt(enc).decode()

    else:
        raise RuntimeError("PROMPT_PASSWORD not set.")
