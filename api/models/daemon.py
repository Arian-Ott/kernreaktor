from db import Base
from sqlalchemy import Column, Integer, String, DateTime, UUID, Boolean, ForeignKey
from uuid import uuid4
from datetime import datetime


class Daemon(Base):
    __tablename__ = "daemons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    client_name = Column(String(32), nullable=False, unique=True)
    client_secret = Column(String(64), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    is_active = Column(Boolean, default=True)


class EncryptionKeypairs(Base):
    __tablename__ = "encryption_keypairs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    public_key = Column(String(255), nullable=False)
    private_key = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    is_active = Column(Boolean, default=True)

    daemon = ForeignKey(
        "daemons", back_populates="encryption_keypairs", ondelete="CASCADE"
    )
