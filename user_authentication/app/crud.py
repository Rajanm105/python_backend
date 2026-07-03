from sqlalchemy.orm import Session

from . import models
from . import schemas

from core.security import hash_password

def get_user_by_email(db: Session, email: str):
    return (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )


def get_user_by_username(db: Session, username: str):
    return (
        db.query(models.User)
        .filter(models.User.username == username)
        .first()
    )

def create_user(db: Session, user: schemas.UserCreate):

    hashed_pw = hash_password(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_pw
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):

    return (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

def get_user_by_email(
    db: Session,
    email: str
):
    return (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )

def update_user(
    db: Session,
    user_id: int,
    user: schemas.UserUpdate
):

    db_user = get_user(db, user_id)

    if not db_user:
        return None

    db_user.username = user.username
    db_user.email = user.email

    db.commit()

    db.refresh(db_user)

    return db_user

def delete_user(
    db: Session,
    user_id: int
):

    db_user = get_user(db, user_id)

    if not db_user:
        return None

    db.delete(db_user)

    db.commit()

    return db_user