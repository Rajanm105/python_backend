from pydantic import BaseModel
from datetime import datetime


class EmailReplyCreate(BaseModel):
    incoming_email: str
    tone: str
    goal: str


class EmailReplyResponse(BaseModel):
    id: int
    incoming_email: str
    tone: str
    goal: str
    generated_reply: str
    created_at: datetime

    class Config:
        from_attributes = True