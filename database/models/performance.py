from sqlalchemy import Column, Integer, Float, DateTime
from database.db import Base
from datetime import datetime

class Performance(Base):
    __tablename__ = "performance"

    id = Column(Integer, primary_key=True)
    realized = Column(Float)
    unrealized = Column(Float)
    equity = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
