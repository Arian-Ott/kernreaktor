from hashlib import sha3_512
from base64 import urlsafe_b64encode, urlsafe_b64decode
from api.crud.daemons import (
    get_daemon,
    get_daemon_by_client_name,
    create_daemon,
    update_daemon,
    delete_daemon,
    get_all_daemons,
    add_encryption_keypair,
    get_daemon_by_name,
)
from api.services.crypto_service import *


def add_daemon(client_name, client_secret):
    """
    Add a new daemon.
    """
    if get_daemon_by_name(client_name):
        raise ValueError("Daemon with this name already exists")

    # Hash the client secret
    hashed_client_secret = sha3_512(client_secret.encode()).hexdigest()

    # Create the daemon
    return create_daemon(client_name, hashed_client_secret)


class DaemonService:
    def __init__(self, daemon_id):
        if not get_daemon(daemon_id):
            raise ValueError("Daemon not found")
        self.daemon_id = daemon_id

    def get_daemon(self):
        return get_daemon(self.daemon_id)

    @staticmethod
    def get_all_daemons():
        return get_all_daemons()

    def update_daemon(self, client_name, client_secret=None, is_active=None):
        """
        Update the daemon's information.
        """
        if client_name:
            # Check if the client name already exists
            existing_daemon = get_daemon_by_client_name(client_name)
            if existing_daemon and existing_daemon["id"] != self.daemon_id:
                raise ValueError("Client name already exists")

        if client_secret:
            # Hash the client secret
            hashed_client_secret = sha3_512(client_secret.encode()).hexdigest()
        else:
            hashed_client_secret = None

        return update_daemon(
            self.daemon_id,
            client_name=client_name,
            client_secret=hashed_client_secret,
            is_active=is_active,
        )

    def delete_daemon(self):
        """
        Delete the daemon.
        """
        return delete_daemon(self.daemon_id)

    def add_encryption_keypair(self, plain_public_key, plain_private_key):
        """
        Add an encryption keypair for the daemon.
        """

        encrypted_public_key = ecies_encrypt(plain_public_key.encode())
        encrypted_private_key = ecies_encrypt(plain_private_key.encode())
        add_encryption_keypair(
            self.daemon_id,
            public_key=encrypted_public_key,
            private_key=encrypted_private_key,
        )

    def add_encrypted_keypair(self, encrypted_data):
        """
        Add an encrypted keypair for the daemon.
        """

        private_key = encrypted_data["private_key"]
        public_key = encrypted_data["public_key"]
        private_key = urlsafe_b64decode(private_key).decode()
        public_key = urlsafe_b64decode(public_key).decode()
        encrypted_data = {"private_key": private_key, "public_key": public_key}
        public_key = ecies_encrypt(encrypted_data["public_key"].encode())
        private_key = ecies_encrypt(encrypted_data["private_key"].encode())
        encrypted_data = {"private_key": private_key, "public_key": public_key}

        add_encryption_keypair(
            self.daemon_id,
            public_key=encrypted_data["public_key"],
            private_key=encrypted_data["private_key"],
        )
