from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=False)
    account_from = Column(String(50), nullable=False)
    account_to = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default="completed")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
