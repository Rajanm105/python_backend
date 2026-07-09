from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.payment import Payment
from app.schemas.payment import (
    CreateOrderRequest,
    CreateOrderResponse,
    VerifyPaymentRequest,
    PaymentStatusResponse,
)
from app.services.razorpay_service import RazorpayService
from app.config import RAZORPAY_KEY_ID

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/create-order", response_model=CreateOrderResponse)
def create_order(payload: CreateOrderRequest, db: Session = Depends(get_db)):
    # Prevent duplicate receipt usage
    existing = db.query(Payment).filter(Payment.receipt == payload.receipt).first()
    if existing:
        raise HTTPException(status_code=400, detail="Receipt already exists")

    razorpay_service = RazorpayService()

    try:
        order = razorpay_service.create_order(
            amount=payload.amount,
            currency=payload.currency,
            receipt=payload.receipt
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create Razorpay order: {str(e)}")

    payment = Payment(
        receipt=payload.receipt,
        amount=payload.amount,
        currency=payload.currency,
        gateway_order_id=order["id"],
        status="created"
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return CreateOrderResponse(
        success=True,
        order_id=order["id"],
        amount=order["amount"],
        currency=order["currency"],
        receipt=payload.receipt,
        key_id=RAZORPAY_KEY_ID,
        status=payment.status
    )


@router.post("/verify")
def verify_payment(payload: VerifyPaymentRequest, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.gateway_order_id == payload.razorpay_order_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment order not found")

    razorpay_service = RazorpayService()

    is_valid = razorpay_service.verify_signature(
        razorpay_order_id=payload.razorpay_order_id,
        razorpay_payment_id=payload.razorpay_payment_id,
        razorpay_signature=payload.razorpay_signature
    )

    if not is_valid:
        payment.status = "failed"
        db.commit()
        raise HTTPException(status_code=400, detail="Invalid payment signature")

    payment.gateway_payment_id = payload.razorpay_payment_id
    payment.gateway_signature = payload.razorpay_signature
    payment.status = "paid"
    payment.paid_at = datetime.utcnow()

    db.commit()
    db.refresh(payment)

    return {
        "success": True,
        "message": "Payment verified successfully",
        "receipt": payment.receipt,
        "order_id": payment.gateway_order_id,
        "payment_id": payment.gateway_payment_id,
        "status": payment.status
    }


@router.get("/{receipt}", response_model=PaymentStatusResponse)
def get_payment_status(receipt: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.receipt == receipt).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return PaymentStatusResponse(
        receipt=payment.receipt,
        amount=payment.amount,
        currency=payment.currency,
        status=payment.status,
        gateway_order_id=payment.gateway_order_id,
        gateway_payment_id=payment.gateway_payment_id,
        created_at=payment.created_at,
        paid_at=payment.paid_at
    )