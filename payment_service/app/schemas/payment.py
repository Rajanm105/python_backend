from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CreateOrderRequest(BaseModel):
    amount: int = Field(..., gt=0, description="Amount in paise")
    currency: str = "INR"
    receipt: str


class CreateOrderResponse(BaseModel):
    success: bool
    order_id: str
    amount: int
    currency: str
    receipt: str
    key_id: str
    status: str


class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class PaymentStatusResponse(BaseModel):
    receipt: str
    amount: int
    currency: str
    status: str
    gateway_order_id: Optional[str] = None
    gateway_payment_id: Optional[str] = None
    created_at: datetime
    paid_at: Optional[datetime] = None