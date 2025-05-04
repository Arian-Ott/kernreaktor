import os
import json
import base64
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


def encrypt(x_b64: str, y_b64: str, payload: str) -> str:
    """
    Encrypts payload using ECDH derived AES key.
    """
    # Entpacke Empfänger-PublicKey (vom TPM generiert)
    x = base64.urlsafe_b64decode(x_b64)
    y = base64.urlsafe_b64decode(y_b64)

    peer_public_numbers = ec.EllipticCurvePublicNumbers(
        int.from_bytes(x, 'big'),
        int.from_bytes(y, 'big'),
        ec.SECP256R1()
    )
    peer_public_key = peer_public_numbers.public_key(default_backend())

    # Erzeuge Ephemeres Schlüsselpaar
    ephemeral_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    ephemeral_public_key = ephemeral_private_key.public_key()

    # ECDH Shared Secret
    shared_secret = ephemeral_private_key.exchange(ec.ECDH(), peer_public_key)

    # Leite AES Schlüssel ab
    aes_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'tpm encryption',
        backend=default_backend()
    ).derive(shared_secret)

    # AES GCM Verschlüsselung
    iv = os.urandom(12)
    encryptor = Cipher(
        algorithms.AES(aes_key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()

    ciphertext = encryptor.update(payload.encode('utf-8')) + encryptor.finalize()

    tag = encryptor.tag

    # Exportiere Ephemeral Public Key
    ephemeral_public_bytes = ephemeral_public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )

    result = {
        "ephemeral_pub": base64.urlsafe_b64encode(ephemeral_public_bytes).decode(),
        "iv": base64.urlsafe_b64encode(iv).decode(),
        "ct": base64.urlsafe_b64encode(ciphertext).decode(),
        "tag": base64.urlsafe_b64encode(tag).decode()
    }

    return base64.urlsafe_b64encode(json.dumps(result).encode('utf-8')).decode('utf-8')

def decrypt(private_key_handle: ESYS_TR, payload: str) -> dict:
    """
    Decrypts payload using TPM's private ECC key via ECDH.
    """
    decoded = base64.urlsafe_b64decode(payload.encode('utf-8'))
    data = json.loads(decoded)

    ephemeral_pub = base64.urlsafe_b64decode(data["ephemeral_pub"])
    iv = base64.urlsafe_b64decode(data["iv"])
    ciphertext = base64.urlsafe_b64decode(data["ct"])
    tag = base64.urlsafe_b64decode(data["tag"])

    # Ephemeral Public Key rekonstruieren
    x = ephemeral_pub[1:33]
    y = ephemeral_pub[33:]

    tpm = ESAPI()

    # Build TPM2B_ECC_POINT
    in_point = TPM2B_ECC_POINT(
        point=TPMS_ECC_POINT(
            x=TPM2B_ECC_PARAMETER(buffer=x),
            y=TPM2B_ECC_PARAMETER(buffer=y)
        )
    )

    # ECDH Shared Secret direkt über TPM berechnen
    z_point = tpm.ECDH_ZGen(private_key_handle, in_point)

    shared_secret = z_point.point.x.buffer  # TPM liefert nur X-Koordinate

    # AES Key ableiten
    aes_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'tpm encryption',
        backend=default_backend()
    ).derive(shared_secret)

    decryptor = Cipher(
        algorithms.AES(aes_key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return json.loads(plaintext.decode('utf-8'))