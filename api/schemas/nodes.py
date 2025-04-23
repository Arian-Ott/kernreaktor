from pydantic import BaseModel, Field
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime


class VMType(str):
    qemu = "qemu"
    lxc = "lxc"


class EnvironmentBase(BaseModel):
    vmid: int
    name: str
    type: Literal["qemu", "lxc"]
    node_name: str
    os_type: Optional[str] = None
    ip_address: Optional[str] = None
    template: Optional[bool] = False
    tags: Optional[str] = None


class EnvironmentCreate(EnvironmentBase):
    pass


class EnvironmentRead(EnvironmentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class StatusSnapshotBase(BaseModel):
    status: str
    uptime: int
    cpu_usage: float
    memory_used: int
    memory_total: int
    disk_used: int
    disk_total: int
    netin_bytes: int
    netout_bytes: int


class StatusSnapshotCreate(StatusSnapshotBase):
    pass


class StatusSnapshotRead(StatusSnapshotBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class VMConfigBase(BaseModel):
    bios: Optional[str] = None
    machine: Optional[str] = None
    scsihw: Optional[str] = None
    iso: Optional[str] = None
    boot_order: Optional[str] = None


class VMConfigCreate(VMConfigBase):
    pass


class LXCConfigBase(BaseModel):
    rootfs: Optional[str] = None
    mounts: Optional[str] = None
    features: Optional[str] = None


class LXCConfigCreate(LXCConfigBase):
    pass
