from pydantic import BaseModel, EmailStr, Field


class UserCreationSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=16)
    password: str = Field(..., min_length=8, max_length=64)


class UserUpdateSchema(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=16)
    password: str | None = Field(None, min_length=8, max_length=64)
    is_active: bool | None = Field(None)
