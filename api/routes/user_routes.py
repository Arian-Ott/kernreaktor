from fastapi import APIRouter, Depends, HTTPException
from schemas.users import UserCreationSchema
from services.user_management import UserService

user_router = APIRouter(default="/users", tags=["users"])


@user_router.post("/register")
async def register_user(user: UserCreationSchema):
    """
    Register a new user.
    """
    try:
        return UserService.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
