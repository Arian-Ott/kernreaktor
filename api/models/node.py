from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from api.db import Base


class Node(Base):
    __tablename__ = "nodes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(64), nullable=False, unique=True, index=True)
    cpus = Column(Integer, nullable=False)
    memory = Column(Integer, nullable=False)
    date_registered = Column(DateTime, nullable=False, default=datetime.now)
    cluster_id = Column(
        Integer,
        ForeignKey("clusters.id"),
        nullable=True,
        ondelete="SET NULL",
        onupdate="CASCADE",
    )
