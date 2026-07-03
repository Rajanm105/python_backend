from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from ..database import get_db

from .. import crud
from .. import schemas
from ..dependencies.auth import get_current_user
from core.security import verify_password, create_access_token

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post(
    "/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_email = crud.get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if username already exists
    existing_username = crud.get_user_by_username(db, user.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    return crud.create_user(db, user)

@router.post(
    "/login",
    response_model=schemas.TokenResponse
)
def login(
    login_data: schemas.LoginRequest,
    db: Session = Depends(get_db)
):
    # Find user by email
    db_user = crud.get_user_by_email(db, login_data.email)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    is_password_valid = verify_password(
        login_data.password,
        db_user.password
    )

    if not is_password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token = create_access_token(
        data={"sub": str(db_user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get(
    "/me",
    response_model=schemas.UserResponse
)
def get_current_logged_in_user(
    current_user = Depends(get_current_user)
):
    return current_user

@router.get(
    "/",
    response_model=list[schemas.UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):
    return crud.get_users(db)




@router.get(
    "/{user_id}",
    response_model=schemas.UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = crud.get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user



@router.put(
    "/{user_id}",
    response_model=schemas.UserResponse
)
def update_user(
    user_id: int,
    updated_user: schemas.UserUpdate,
    db: Session = Depends(get_db)
):

    user = crud.update_user(
        db,
        user_id,
        updated_user
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = crud.delete_user(
        db,
        user_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }