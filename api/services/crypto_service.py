import os
from pathlib import Path
from base64 import urlsafe_b64encode, urlsafe_b64decode
from pprint import pprint

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend


KEY_DIR = Path(__file__).parent.parent / "keys"
PRIVATE_KEY_FILE = KEY_DIR / "private_key.pem"
PUBLIC_KEY_FILE = KEY_DIR / "public_key.pem"


def generate_keys():
    """
    Generates a 4096-bit RSA key pair and saves them in the 'keys/' directory.
    """
    KEY_DIR.mkdir(parents=True, exist_ok=True)

    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=4096, backend=default_backend()
    )

    with open(PRIVATE_KEY_FILE, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    with open(PUBLIC_KEY_FILE, "wb") as f:
        f.write(
            private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )


def server_encrypt(plaintext: str) -> str:
    """
    Encrypts a string using the server's RSA public key.
    Returns the encrypted Base64 string.
    """
    with open(PUBLIC_KEY_FILE, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    ciphertext = public_key.encrypt(
        plaintext.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return urlsafe_b64encode(ciphertext).decode("utf-8")


def decrypt(ciphertext_b64: str):
    """
    Decrypts a Base64-encoded string using the server's RSA private key.
    Returns the original plaintext.
    """

    ciphertext = urlsafe_b64decode(ciphertext_b64)

    with open(PRIVATE_KEY_FILE, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(), password=None, backend=default_backend()
        )

    plaintext_bytes = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return plaintext_bytes
