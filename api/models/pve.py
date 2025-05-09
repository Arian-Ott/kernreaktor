from api.db import Base
from sqlalchemy import (
    UUID,
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
)
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid


class VMType(enum.Enum):
    qemu = "qemu"
    lxc = "lxc"


class Cluster(Base):
    __tablename__ = "clusters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    cluster_hostname = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Node(Base):
    __tablename__ = "nodes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    node_name = Column(String(255), nullable=False)
    cluster_id = Column(
        UUID(as_uuid=True), ForeignKey("clusters.id", ondelete="CASCADE")
    )
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class NodeSpecs(Base):
    __tablename__ = "node_specs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    node_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id", ondelete="CASCADE"))
    cpu_cores = Column(Integer)
    memory_total = Column(Integer)
    disk_total = Column(Integer)
    disk_used = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class NodeEnvironment(Base):
    __tablename__ = "node_environments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hostname = Column(String(255), nullable=False, unique=True)
    ipv4_address = Column(String(64), nullable=False, unique=True)
    assigned_cores = Column(Integer)
    assigned_memory = Column(Integer)
    assigned_disk = Column(Integer)
    used_disk = Column(Integer)
    node_id = Column(
        UUID(as_uuid=True), ForeignKey("nodes.id", ondelete="CASCADE"), nullable=True
    )

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    environment_type = Column(Enum(VMType), nullable=False)
    automigration = Column(Boolean, default=False)


class NodeUsageLog(Base):
    __tablename__ = "node_usage_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    node_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id", ondelete="CASCADE"))
    cpu_usage = Column(Integer)
    memory_usage = Column(Integer)
    disk_usage = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
