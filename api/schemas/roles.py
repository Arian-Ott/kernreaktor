from pydantic import BaseModel


class RoleBaseSchema(BaseModel):
    name: str
    description: str | None = None
