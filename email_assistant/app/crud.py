from sqlalchemy.orm import Session

from . import models
from . import schemas


def create_email_reply(
    db: Session,
    email_data: schemas.EmailReplyCreate,
    generated_reply: str
):
    db_email = models.EmailReply(
        incoming_email=email_data.incoming_email,
        tone=email_data.tone,
        goal=email_data.goal,
        generated_reply=generated_reply
    )

    db.add(db_email)
    db.commit()
    db.refresh(db_email)

    return db_email


def get_email_replies(db: Session):
    return db.query(models.EmailReply).all()


def get_email_reply(db: Session, email_id: int):
    return (
        db.query(models.EmailReply)
        .filter(models.EmailReply.id == email_id)
        .first()
    )


def delete_email_reply(db: Session, email_id: int):
    db_email = get_email_reply(db, email_id)

    if not db_email:
        return None

    db.delete(db_email)
    db.commit()

    return db_email