import os
import base64
from getpass import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

prompt = f"""
You are a git commit analyzer. You MUST analyze this ENTIRE commit history CAREFULLY and find any secret/confidential data inside. 
Do NOT invent anything. For each finding output exactly this JSON array format:

[
  {{
    "commit": "<commit-hash>",
    "file": "<path/to/file>",
    "line": <line_number>,
    "snippet": "<text of the line>",
    "finding_type": "<what kind of line have you found>"
    "rationale": "<why is this line suspicious>",
    "Automated detection": true
  }},
  ...
]

If nothing suspicious is found, output exactly:
[]
"""

password = getpass("Enter a password to encrypt the prompt: ")

salt = os.urandom(16)

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390_000,
)
key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

f = Fernet(key)
enc = f.encrypt(prompt.encode())

with open("prompt.enc", "wb") as fh:
    fh.write(enc)

with open("prompt.salt", "wb") as fh:
    fh.write(salt)

print("✅ prompt.enc and prompt.salt created successfully.")
print("⚠️ Remember to give the password to the user securely (do NOT commit the password).")
