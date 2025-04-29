from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os
from base64 import urlsafe_b64decode, urlsafe_b64encode
from config import settings


def generate_ec_key_pair() -> tuple[
    ec.EllipticCurvePrivateKey, ec.EllipticCurvePublicKey
]:
    """
    Generates a new ECC key pair (SECP256R1),
    saves them to 'keys/private.key' and 'keys/public.pem',
    and returns (private_key, public_key).
    """
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    return private_key, public_key


def load_private_key() -> ec.EllipticCurvePrivateKey:
    """
    Loads the private key from 'keys/private.key'.
    """
    with open("keys/private.key", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(), password=None, backend=default_backend()
        )
    return private_key


def load_public_key() -> ec.EllipticCurvePublicKey:
    """
    Loads the public key from 'keys/public.pem'.
    """
    with open("keys/public.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(
            f.read(), backend=default_backend()
        )
    return public_key


def derive_aes_key(shared_key: bytes) -> bytes:
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt="".encode(),
        info=b"ecies-encryption",
    ).derive(shared_key)


def ecies_encrypt(plaintext: bytes) -> dict:
    """
    Encrypts plaintext using the public key from 'keys/public.pem'.
    """
    recipient_public_key = load_public_key()

    ephemeral_private_key = ec.generate_private_key(ec.SECP256R1())
    ephemeral_public_key = ephemeral_private_key.public_key()

    shared_key = ephemeral_private_key.exchange(ec.ECDH(), recipient_public_key)
    aes_key = derive_aes_key(shared_key)

    iv = os.urandom(12)
    encryptor = Cipher(algorithms.AES(aes_key), modes.GCM(iv)).encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    ephemeral_public_bytes = ephemeral_public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint,
    )

    return {
        "ephemeral_public_key": urlsafe_b64encode(ephemeral_public_bytes).decode(),
        "iv": urlsafe_b64encode(iv).decode(),
        "ciphertext": urlsafe_b64encode(ciphertext).decode(),
        "tag": urlsafe_b64encode(encryptor.tag).decode(),
    }


def ecies_decrypt(data: dict) -> bytes:
    """
    Decrypts the encrypted data using the private key from 'keys/private.key'.
    """
    recipient_private_key = load_private_key()

    ephemeral_public_key = ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP256R1(), data["ephemeral_public_key"]
    )

    shared_key = recipient_private_key.exchange(ec.ECDH(), ephemeral_public_key)
    aes_key = derive_aes_key(shared_key)

    decryptor = Cipher(
        algorithms.AES(aes_key), modes.GCM(data["iv"], data["tag"])
    ).decryptor()
    plaintext = decryptor.update(data["ciphertext"]) + decryptor.finalize()

    return plaintext
