import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from base64 import urlsafe_b64encode, urlsafe_b64decode
from pprint import pprint
from pathlib import Path
def generate_keys():
    """
    Generiert ein RSA 4096 Schlüsselpaar und speichert sie unverschlüsselt im Verzeichnis 'keys/'.
    """
    key_dir = Path(__file__).parent/"keys"
    if not os.path.exists(key_dir):
        os.makedirs(key_dir)

   
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
   
    )

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    
    )

    public_key = private_key.public_key()

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    
    )
    return private_bytes, public_bytes
    # Schlüssel speichern
    


def server_encrypt(plaintext: str) -> bytes:
    """
    Verschlüsselt einen String mit dem RSA Public Key.

    :param plaintext: Der zu verschlüsselnde String
    :param key_dir: Verzeichnis, wo der öffentliche Schlüssel liegt
    :param public_key_file: Dateiname des öffentlichen Schlüssels
    :return: Verschlüsselte Daten (Bytes)
    """
    key_dir = "keys"
   
    public_key_file = "public.pem"
    public_key_path = os.path.join(key_dir, public_key_file)
    print(plaintext)
    # Public Key laden
    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # String in Bytes umwandeln
    plaintext_bytes = plaintext.encode("utf-8")

    # Verschlüsseln mit Padding OAEP
    ciphertext = public_key.encrypt(
        plaintext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    ciphertext = urlsafe_b64encode(ciphertext).decode("utf-8")
    return ciphertext

def decrypt(ciphertext):
    pprint("decrypt", ciphertext)
    ciphertext = urlsafe_b64decode(ciphertext.encode()).decode()
    key_dir = "keys"
    private_key_file = "private.pem"
    private_key_path = os.path.join(key_dir, private_key_file)
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
       
        )

    # Entschlüsseln
    plaintext_bytes = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(plaintext_bytes)
    return plaintext_bytes.decode("utf-8")