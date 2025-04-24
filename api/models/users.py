from api.db import Base
from sqlalchemy import Column, Boolean, String, DateTime, UUID
import uuid
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    is_active = Column(Boolean, default=True)
