import os
import base64
from getpass import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

prompt = f"""
You are a git commit analyzer. Analyze ONLY the commit history and its diffs that I provide.
Your goal is to detect any secrets or confidential data introduced.

Definitions:
- Secret/confidential value (finding_type = 0): API keys, passwords, tokens, private keys, certificates, credentials inside code or config.
- Confidential file (finding_type = 1): files such as `.env`, `.pem`, `.key`, `.crt`, `id_rsa`, `config.json` with secrets, or similar.

Rules:
- Base your analysis strictly on the commit data provided. Do NOT invent values or paths.
- Output ONLY a JSON array in this exact format, no explanations outside it.
- If nothing suspicious is found, return exactly: []

JSON schema for each finding:
[
  {{
    "commit": "<commit-hash>",
    "file": "<path/to/file>",
    "line": <line_number>,       // integer line number in diff context
    "snippet": "<text of the line>", 
    "finding_type": 0 or 1,      // 0 = secret value, 1 = confidential file
    "rationale": "<short reason why this line or file is suspicious>",
    "Automated detection": true
  }},
  ...
]

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
