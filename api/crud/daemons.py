from models.daemon import Daemon, EncryptionKeypairs
from db import get_db

def get_daemon(daemon_id):
    db = next(get_db())
    return db.query(Daemon).filter(Daemon.id == daemon_id).first()

def get_daemon_by_client_name(client_name):
    db = next(get_db())
    return db.query(Daemon).filter(Daemon.client_name == client_name).first()

def create_daemon(client_name, client_secret):
    db = next(get_db())
    new_daemon = Daemon(client_name=client_name, client_secret=client_secret)
    db.add(new_daemon)
    db.commit()
    db.refresh(new_daemon)
    return new_daemon

def update_daemon(daemon_id, client_name=None, client_secret=None, is_active=None):
    db = next(get_db())
    daemon = db.query(Daemon).filter(Daemon.id == daemon_id).first()
    if not daemon:
        return None
    if client_name:
        daemon.client_name = client_name
    if client_secret:
        daemon.client_secret = client_secret
    if is_active is not None:
        daemon.is_active = is_active
    db.commit()
    db.refresh(daemon)
    return daemon

def delete_daemon(daemon_id):
    db = next(get_db())
    daemon = db.query(Daemon).filter(Daemon.id == daemon_id).first()
    if not daemon:
        return None
    db.delete(daemon)
    db.commit()
    return daemon

def get_all_daemons():
    db = next(get_db())
    return db.query(Daemon).all()

def add_encryption_keypair(daemon_id, public_key, private_key):
    db = next(get_db())
    new_keypair = EncryptionKeypairs(
        public_key=public_key,
        private_key=private_key,
        daemon_id=daemon_id
    )
    db.add(new_keypair)
    db.commit()
    db.refresh(new_keypair)
    return new_keypair

def delete_encryption_keypair(keypair_id):
    db = next(get_db())
    keypair = db.query(EncryptionKeypairs).filter(EncryptionKeypairs.id == keypair_id).first()
    if not keypair:
        return None
    db.delete(keypair)
    db.commit()
    return keypair

def get_encryption_keypair(keypair_id: None | str = None, daemon_id: None | str = None):
    db = next(get_db())
    if keypair_id:
        return db.query(EncryptionKeypairs).filter(EncryptionKeypairs.id == keypair_id).first()
    elif daemon_id:
        return db.query(EncryptionKeypairs).filter(EncryptionKeypairs.daemon_id == daemon_id).first()
    else:
        raise ValueError("Either keypair_id or daemon_id must be provided")
    
def get_daemon_by_name(client_name: str):
    db = next(get_db())
    return db.query(Daemon).filter(Daemon.client_name == client_name).first()