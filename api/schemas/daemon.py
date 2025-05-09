from pydantic import BaseModel, Field, UUID4


class DaemonCreationSchema(BaseModel):
    client_name: str
    client_secret: str


class DaemonIDSchema(BaseModel):
    client_id: str | UUID4
