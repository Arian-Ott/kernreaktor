from db import get_db
from models.users import User


def get_user(user_id):
    db = next(get_db())
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(username):
    db = next(get_db())
    return db.query(User).filter(User.username == username).first()


def create_user(username, password):
    db = next(get_db())
    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users():
    db = next(get_db())
    return db.query(User).all()


def update_user(user_id, username=None, password=None, is_active=None):
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    if username:
        user.username = username
    if password:
        user.password = password
    if is_active is not None:
        user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user


def delete_user(user_id):
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user
