from api.crud.roles import *

from api.models.users import User, UserRoles
from api.schemas.roles import RoleBaseSchema
from api.services.hash_utils import hash_password
from api.db import get_db, Base, engine
from api.services.crypto_service import generate_keys
import logging
import os
from pathlib import Path


def create_roles():
    roles = [
        {"name": "admin", "description": "Administrator"},
        {"name": "user", "description": "Regular user"},
        {"name": "guest", "description": "Guest user"},
        {"name": "technical", "description": "technical user"},
    ]
    for role in roles:
        if get_role(role["name"]):
            continue
        try:
            lo_role = RoleBaseSchema(**role)

            create_role(lo_role)

        except Exception as e:
            logging.error(f"Error creating role {role['name']}: {e}")
            continue


def create_admin_user():
    db = next(get_db())
    # Check if the admin user already exists
    existing_user = db.query(User).filter(User.username == "admin").first()
    if not existing_user:
        try:
            new_user = User(username="admin", password=hash_password("changememf"))
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except Exception as e:
            logging.error(f"Error creating admin user: {e}")
        try:
            new_user_role = UserRoles(user_id=new_user.id, role_name="admin")
            db.add(new_user_role)
            db.commit()
            db.refresh(new_user_role)
        except Exception as e:
            logging.error(f"Error assigning admin role to user: {e}")


def key_generation():
    if not os.path.exists(Path(__file__).parent.parent / "keys"):
        os.makedirs(Path(__file__).parent.parent / "keys")
    if not os.path.exists(
        Path(__file__).parent.parent / "keys/private_key.pem"
    ) and not os.path.exists(Path(__file__).parent.parent / "keys/public_key.pem"):
        try:
            private, public = generate_keys()
            with open(Path(__file__).parent.parent / "keys/private_key.pem", "wb") as f:
                f.write(private)
            with open(Path(__file__).parent.parent / "keys/public_key.pem", "wb") as f:
                f.write(public)
        except Exception as e:
            logging.error(f"Error generating keys: {e}")


def startup_tasks():
    """
    Startup tasks for the FastAPI application.
    This function is called when the application starts.
    """
    Base.metadata.create_all(bind=engine)
    key_generation()
    create_roles()
    create_admin_user()
