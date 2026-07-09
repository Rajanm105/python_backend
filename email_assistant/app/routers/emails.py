from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import crud, schemas
from ..services.ai_email_service import generate_email_reply

router = APIRouter(
    prefix="/emails",
    tags=["Emails"]
)


@router.post("/generate", response_model=schemas.EmailReplyResponse)
def generate_email(
    email_data: schemas.EmailReplyCreate,
    db: Session = Depends(get_db)
):
    reply_text = generate_email_reply(
        incoming_email=email_data.incoming_email,
        tone=email_data.tone,
        goal=email_data.goal
    )

    saved_email = crud.create_email_reply(
        db,
        email_data,
        reply_text
    )

    return saved_email


@router.get("/", response_model=list[schemas.EmailReplyResponse])
def get_all_emails(db: Session = Depends(get_db)):
    return crud.get_email_replies(db)


@router.get("/{email_id}", response_model=schemas.EmailReplyResponse)
def get_one_email(
    email_id: int,
    db: Session = Depends(get_db)
):
    email = crud.get_email_reply(db, email_id)

    if not email:
        raise HTTPException(
            status_code=404,
            detail="Email reply not found"
        )

    return email


@router.delete("/{email_id}")
def delete_email(
    email_id: int,
    db: Session = Depends(get_db)
):
    email = crud.delete_email_reply(db, email_id)

    if not email:
        raise HTTPException(
            status_code=404,
            detail="Email reply not found"
        )

    return {
        "message": "Email reply deleted successfully"
    }