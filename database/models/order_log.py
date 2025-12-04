from sqlalchemy import Column, Integer, String, Float, DateTime
from database.db import Base
from datetime import datetime

class OrderLog(Base):
    __tablename__ = "order_logs"

    id = Column(Integer, primary_key=True)
    exchange = Column(String)
    side = Column(String)
    size = Column(Float)
    price = Column(Float)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
