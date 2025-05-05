from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from enum import Enum
from typing import Optional


class VMType(str, Enum):
    qemu = "qemu"
    lxc = "lxc"


class ClusterBase(BaseModel):
    cluster_hostname: str = Field(..., max_length=255)


class ClusterCreate(ClusterBase):
    pass


class ClusterUpdate(BaseModel):
    cluster_hostname: Optional[str] = None


class ClusterOut(ClusterBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class NodeBase(BaseModel):
    node_name: str = Field(..., max_length=255)
    cluster_id: UUID


class NodeCreate(NodeBase):
    pass


class NodeUpdate(BaseModel):
    node_name: Optional[str] = None
    cluster_id: Optional[UUID] = None


class NodeOut(NodeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class NodeSpecsBase(BaseModel):
    node_id: UUID
    cpu_cores: int
    memory_total: int
    disk_total: int
    disk_used: int


class NodeSpecsCreate(NodeSpecsBase):
    pass


class NodeSpecsUpdate(BaseModel):
    cpu_cores: Optional[int] = None
    memory_total: Optional[int] = None
    disk_total: Optional[int] = None
    disk_used: Optional[int] = None


class NodeSpecsOut(NodeSpecsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class NodeEnvironmentBase(BaseModel):
    hostname: str
    ipv4_address: str
    assigned_cores: int
    assigned_memory: int
    assigned_disk: int
    used_disk: int
    node_id: UUID
    environment_id: UUID
    environment_type: VMType
    automigration: Optional[bool] = False


class NodeEnvironmentCreate(NodeEnvironmentBase):
    pass


class NodeEnvironmentUpdate(BaseModel):
    hostname: Optional[str] = None
    ipv4_address: Optional[str] = None
    assigned_cores: Optional[int] = None
    assigned_memory: Optional[int] = None
    assigned_disk: Optional[int] = None
    used_disk: Optional[int] = None
    node_id: Optional[UUID] = None
    environment_id: Optional[UUID] = None
    environment_type: Optional[VMType] = None
    automigration: Optional[bool] = None


class NodeEnvironmentOut(NodeEnvironmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ----------------------- NodeUsageLog -----------------------


class NodeUsageLogBase(BaseModel):
    node_id: UUID
    cpu_usage: int
    memory_usage: int
    disk_usage: int


class NodeUsageLogCreate(NodeUsageLogBase):
    pass


class NodeUsageLogOut(NodeUsageLogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
