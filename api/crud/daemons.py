from api.models.daemon import Daemon
from api.db import get_db

def get_daemon(daemon_id):
    db = get_db()
    return db.query(Daemon).filter(Daemon.id == daemon_id).first()

def get_daemon_by_client_name(client_name):
    db = get_db()
    return db.query(Daemon).filter(Daemon.client_name == client_name).first()
def create_daemon(client_name, client_secret):
    db = get_db()
    new_daemon = Daemon(client_name=client_name, client_secret=client_secret)
    db.add(new_daemon)
    db.commit()
    db.refresh(new_daemon)
    return new_daemon

def update_daemon(daemon_id, client_name=None, client_secret=None, is_active=None):
    db = get_db()
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
    db = get_db()
    daemon = db.query(Daemon).filter(Daemon.id == daemon_id).first()
    if not daemon:
        return None
    db.delete(daemon)
    db.commit()
    return daemon
def get_all_daemons():
    db = get_db()
    return db.query(Daemon).all()