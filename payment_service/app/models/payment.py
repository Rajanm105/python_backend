from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    receipt = Column(String, unique=True, nullable=False, index=True)
    amount = Column(Integer, nullable=False)  # amount in paise
    currency = Column(String, default="INR", nullable=False)

    gateway_order_id = Column(String, unique=True, nullable=True, index=True)
    gateway_payment_id = Column(String, nullable=True)
    gateway_signature = Column(String, nullable=True)

    status = Column(String, default="created", nullable=False)  # created, paid, failed

    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)