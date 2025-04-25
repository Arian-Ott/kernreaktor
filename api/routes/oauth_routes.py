from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from services.user_management import UserService
from config import settings
from uuid import UUID

router = APIRouter(prefix="/oauth", tags=["OAuth2"])

# Dummy user database


# Security and token setup
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS512"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dependencies
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/oauth/token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if "role" and "user_id" in payload:
            if UserService.get_user(user_id=UUID(payload.get("sub"))) is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return {"user_id": payload.get("sub"), "role": payload.get("role")}
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = UserService.get_user(username=form_data.username)
    print(user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not UserService.verify_password(user.id, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"message": f"Hello, {username}"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/me")
async def get_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = UserService.get_user(user_id=UUID(user_id))
        del user.password
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
