from fastapi import APIRouter, Depends, HTTPException
from api.schemas.users import UserCreationSchema
from api.services.user_management import UserService
from jose import JWTError, jwt

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/register")
async def register_user(user: UserCreationSchema):
    """
    Register a new user.
    """
    try:
        return UserService.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
