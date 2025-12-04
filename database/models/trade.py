from sqlalchemy import Column, Integer, Float, String, DateTime
from database.db import Base
from datetime import datetime

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    side = Column(String)
    size = Column(Float)
    entry = Column(Float)
    exit = Column(Float)
    pnl = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
