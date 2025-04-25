from crud.roles import create_role
from models.users import User, UserRoles
from schemas.roles import RoleBaseSchema
from services.hash_utils import hash_password
from db import get_db


def create_roles():
    roles = [
        {"name": "admin", "description": "Administrator"},
        {"name": "user", "description": "Regular user"},
        {"name": "guest", "description": "Guest user"},
        {"name": "technical", "description": "technical user"},
    ]
    for role in roles:
        lo_role = RoleBaseSchema(**role)
        create_role(lo_role)


def create_admin_user():
    db = next(get_db())
    # Check if the admin user already exists
    existing_user = db.query(User).filter(User.username == "admin").first()
    if not existing_user:
        new_user = User(username="admin", password=hash_password("changememf"))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        new_user_role = UserRoles(user_id=new_user.id, role_name="admin")
        db.add(new_user_role)
        db.commit()
        db.refresh(new_user_role)


def startup_tasks():
    """
    Startup tasks for the FastAPI application.
    This function is called when the application starts.
    """
    create_roles()
    create_admin_user()
