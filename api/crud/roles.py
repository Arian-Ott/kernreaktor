from api.models.users import User, Roles, UserRoles
from api.schemas.roles import RoleBaseSchema
from api.db import get_db
from api.crud.users import get_user


def create_role(role: RoleBaseSchema):
    db = next(get_db())
    new_role = Roles(name=role.name, description=role.description)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


def get_role(role_name):
    db = next(get_db())
    return db.query(Roles).filter(Roles.name == role_name).first()


def get_roles():
    db = next(get_db())
    return db.query(Roles).all()


def get_usr_roles(user_id):
    db = next(get_db())
    return db.query(UserRoles).filter(UserRoles.user_id == user_id).all()


def delete_role(role_name):
    db = next(get_db())
    role = db.query(Roles).filter(Roles.name == role_name).first()
    if not role:
        return None
    db.delete(role)
    db.commit()
    return role


def assign_role_to_user(user_id, role_name):
    db = next(get_db())
    user_role = UserRoles(user_id=user_id, role_name=role_name)
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    return user_role


def unassign_role_from_user(user_id, role_name):
    db = next(get_db())
    role = db.query(UserRoles).filter
    db.refresh()
