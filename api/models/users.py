from api.db import Base
from sqlalchemy import Column, Boolean, String, DateTime, UUID, Integer, ForeignKey
import uuid
from datetime import datetime

from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(32), nullable=False, unique=True, index=True)
    password = Column(String(128), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    is_active = Column(Boolean, default=True)

    roles = relationship(
        "UserRoles", back_populates="user", cascade="all, delete-orphan"
    )


class Roles(Base):
    __tablename__ = "roles"
    name = Column(String(32), nullable=False, unique=True, primary_key=True, index=True)
    description = Column(String(255))

    users = relationship(
        "UserRoles", back_populates="role", cascade="all, delete-orphan"
    )


class UserRoles(Base):
    __tablename__ = "user_roles"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    role_name = Column(
        String(32),
        ForeignKey("roles.name", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    user = relationship("User", back_populates="roles")
    role = relationship("Roles", back_populates="users")
