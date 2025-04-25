from db import Base
from sqlalchemy import Column, String, DateTime, UUID, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from uuid import uuid4


class LogLevels(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"
    CRITICAL = "critical"
    TRACE = "trace"


class EnvironmentLog(Base):
    __tablename__ = "environment_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    level = Column(Enum(LogLevels), nullable=False)
    message = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    environment = Column(UUID(as_uuid=True), ForeignKey("environments.id"))


class UserLog(Base):
    __tablename__ = "user_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    level = Column(Enum(LogLevels), nullable=False)
    message = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="logs")
