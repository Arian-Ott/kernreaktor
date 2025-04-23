from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum, ForeignKey, Text, CHAR, UUID, Float, BigInteger
from sqlalchemy.orm import relationship
from api.db import Base
from datetime import datetime
import enum
import uuid

class VMType(enum.Enum):
    qemu = "qemu"
    lxc = "lxc"

class Environment(Base):
    __tablename__ = "environments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vmid = Column(Integer, nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum(VMType), nullable=False)
    node_name = Column(String(255), nullable=False)
    os_type = Column(String(64))
    ip_address = Column(String(64))
    template = Column(Boolean, default=False)
    tags = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    vm_config = relationship("VMConfig", back_populates="environment", uselist=False)
    lxc_config = relationship("LXCConfig", back_populates="environment", uselist=False)
    status_snapshots = relationship("StatusSnapshot", back_populates="environment", cascade="all, delete-orphan")
    
class LXCConfig(Base):
    __tablename__ = "lxc_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    environment_id = Column(UUID(as_uuid=True), ForeignKey("environments.id", ondelete="CASCADE"))
    rootfs = Column(String(255))
    mounts = Column(Text)
    features = Column(Text)

    environment = relationship("Environment", back_populates="lxc_config")
    
class StatusSnapshot(Base):
    __tablename__ = "status_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    environment_id = Column(UUID(as_uuid=True), ForeignKey("environments.id", ondelete="CASCADE"))
    status = Column(String(32))
    uptime = Column(Integer)
    cpu_usage = Column(Float)
    memory_used = Column(BigInteger)
    memory_total = Column(BigInteger)
    disk_used = Column(BigInteger)
    disk_total = Column(BigInteger)
    netin_bytes = Column(BigInteger)
    netout_bytes = Column(BigInteger)
    created_at = Column(DateTime, default=datetime.now)

    environment = relationship("Environment", back_populates="status_snapshots")
    
    
class VMConfig(Base):
    __tablename__ = "vm_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    environment_id = Column(UUID(as_uuid=True), ForeignKey("environments.id", ondelete="CASCADE"))
    bios = Column(String(64))
    machine = Column(String(64))
    scsihw = Column(String(64))
    iso = Column(String(255))
    boot_order = Column(String(32))

    environment = relationship("Environment", back_populates="vm_config")