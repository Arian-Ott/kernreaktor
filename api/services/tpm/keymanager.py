import os
import sys
import base64
from pathlib import Path
import pgpy
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm
import uuid
TPM_PERSISTENT_HANDLE = 0x81010001
KEYS_DIR = Path("keys")
PRIVATE_KEY_FILE = KEYS_DIR / "private_key.asc"
PUBLIC_KEY_FILE = KEYS_DIR / "public_key.asc"

if sys.platform == "linux" or sys.platform == "linux2":
    TPM_AVAILABLE = True
else:
    TPM_AVAILABLE = False


class TPMKeyManager:
    def __init__(self):
        KEYS_DIR.mkdir(exist_ok=True)
        if not PRIVATE_KEY_FILE.exists() or not PUBLIC_KEY_FILE.exists():
            self._create_gpg_key()

    def _create_gpg_key(self):
        """
        Erzeugt einen echten GPG Schlüssel (PGP Key) im ECC Format
        """
        tmp_uuid = str(uuid.uuid4())
        key = pgpy.PGPKey.new(PubKeyAlgorithm.ECDSA, curve='NIST P-256')
        uid = pgpy.PGPUID.new(f"kernreaktor:sys:{tmp_uuid}", email=f'kernreaktor-sys-{tmp_uuid}@example.com')

        key.add_uid(
            uid,
            usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
            hashes=[HashAlgorithm.SHA256],
            ciphers=[SymmetricKeyAlgorithm.AES256],
            compression=[CompressionAlgorithm.ZLIB]
        )

        # Speichern Public und Private
        with open(PRIVATE_KEY_FILE, "w") as f:
            f.write(str(key))

        with open(PUBLIC_KEY_FILE, "w") as f:
            f.write(str(key.pubkey))

    def create_and_store_key(self):
        """
        Lädt den Public Key und gibt (x, y) base64 zurück
        """
        pubkey, _ = pgpy.PGPKey.from_file(str(PUBLIC_KEY_FILE))

        ecpub = pubkey._key.keymaterial

        x = base64.urlsafe_b64encode(ecpub.Q.x.to_bytes(32, byteorder='big')).decode()
        y = base64.urlsafe_b64encode(ecpub.Q.y.to_bytes(32, byteorder='big')).decode()

        return x, y

    def load_key_handle(self):
        """
        Lädt den Private Key
        """
        privkey, _ = pgpy.PGPKey.from_file(str(PRIVATE_KEY_FILE))
        return privkey