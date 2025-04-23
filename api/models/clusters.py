from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime   
from api.db import Base

class Cluster(Base):
    __tablename__ = "clusters"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(64), nullable=False, unique=True, index=True)
    description = Column(String(256), nullable=True)
    date_registered = Column(DateTime, nullable=True, default=datetime.now)
