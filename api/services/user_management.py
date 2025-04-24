from sqlalchemy.orm import Session
from schemas.users import UserCreationSchema
from crud import users as crud_users
from uuid import UUID
from services.hash_utils import hash_password, verify_password


class UserService:
    def __init__(self):
        if len(UserService.get_all_users()) == 0:
            # Create a default admin user if no users exist
            crud_users.create_user("admin", hash_password("admin"))

    @staticmethod
    def create_user(user: UserCreationSchema):
        """
        Create a new user in the database.
        """
        if crud_users.get_user_by_username(user.username):
            raise ValueError("Username already exists")
        user.password = hash_password(user.password)

        return crud_users.create_user(user.username, user.password)

    @staticmethod
    def get_user(user_id: UUID | None = None, username: str | None = None):
        """
        Get a user by ID or username.
        """
        if user_id:
            return crud_users.get_user(user_id)
        elif username:
            return crud_users.get_user_by_username(username)
        else:
            raise ValueError("Either user_id or username must be provided")

    @staticmethod
    def get_all_users():
        """
        Get all users.
        """
        return crud_users.get_all_users()

    @staticmethod
    def delete_user(user_id: UUID | None = None, username: str | None = None):
        """
        Delete a user by ID.
        """
        if user_id:
            user = UserService.get_user(user_id=user_id)
        elif username:
            user = UserService.get_user(username=username)
        else:
            raise ValueError("Either user_id or username must be provided")
        if not user:
            raise ValueError("User not found")
        crud_users.delete_user(user.id)

    @staticmethod
    def update_user(
        user_id: UUID | None = None,
        username: str | None = None,
        password: str | None = None,
        is_active: bool | None = None,
    ):
        """
        Update a user by ID.
        """
        if user_id:
            user = UserService.get_user(user_id=user_id)
        elif username:
            user = UserService.get_user(username=username)
        else:
            raise ValueError("Either user_id or username must be provided")
        if not user:
            raise ValueError("User not found")
        if password:
            password = hash_password(password)
        crud_users.update_user(
            user.id, username=username, password=password, is_active=is_active
        )

    @staticmethod
    def verify_password(user_id: UUID, password: str):
        """
        Verify a user's password.
        """
        user = UserService.get_user(user_id=user_id)
        if not user:
            raise ValueError("User not found")
        return verify_password(password, user.password)
