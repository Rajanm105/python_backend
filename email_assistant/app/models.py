from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

from .database import Base


class EmailReply(Base):
    __tablename__ = "email_replies"

    id = Column(Integer, primary_key=True, index=True)
    incoming_email = Column(Text, nullable=False)
    tone = Column(String, nullable=False)
    goal = Column(String, nullable=False)
    generated_reply = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)