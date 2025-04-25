from functools import wraps
from fastapi import Request
from fastapi import Depends, HTTPException, status
from routes.oauth_routes import get_current_user
from crud.users import get_user
from crud.roles import get_usr_roles, get_role, assign_role_to_user


def require_roles(*allowed_roles):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, user=Depends(get_current_user), **kwargs):
            if user["role"] not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied for role: {user['role']}",
                )
            return await func(*args, user=user, **kwargs)

        return wrapper

    return decorator


class RoleService:
    @staticmethod
    def get_user_roles(user_id):
        if not get_user(user_id):
            raise ValueError("User not found")

        return get_usr_roles(user_id)

    @staticmethod
    def set_user_role(user_id, role):
        user = get_user(user_id)
        role = get_role(role)
        if not user:
            raise ValueError("User not found")

        if not role:
            raise ValueError("Role not found")

        resp = assign_role_to_user(user.id, role.name)
        return resp

    @staticmethod
    def delete_user_role(user_id, role):
        user = get_user(user_id)
        role = get_role(role)
        if not user:
            raise ValueError("User not found")
        if not role:
            raise ValueError("Role not found")
