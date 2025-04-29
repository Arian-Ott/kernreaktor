from api.crud.roles import create_role, get_role
from api.models.users import User, UserRoles
from api.schemas.roles import RoleBaseSchema
from api.services.hash_utils import hash_password
from api.db import get_db

import logging
import os



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


def create_encryption_keypair():
    if os.path.exists("keys/private.pem") and os.path.exists("keys/public.pem"):
        logging.info("Encryption keypair already exists.")
        return
    os.makedirs("keys", exist_ok=True)
    private_key, public_key = generate_ec_key_pair()

    with open("keys/private.key", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    with open("keys/public.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )


def startup_tasks():
    """
    Startup tasks for the FastAPI application.
    This function is called when the application starts.
    """
    Base.metadata.create_all(bind=engine)   
    create_encryption_keypair()
    create_roles()
    create_admin_user()
