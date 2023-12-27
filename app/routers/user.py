from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import database, models, schemas, security

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(
    user: schemas.UserIn, db: Session = Depends(database.get_db)
) -> schemas.UserOut:
    password_hash = security.pwd_context.hash(user.password)
    user = models.User(email=user.email, password_hash=password_hash)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="User with this email already exists."
        )
    db.refresh(user)
    return user


@router.get("/me")
def get_user_me(
    current_user: models.User = Depends(security.get_current_user),
) -> schemas.UserOut:
    return current_user


@router.get("/{id}")
def get_user(id: int, db: Session = Depends(database.get_db)) -> schemas.UserOut:
    stmt = select(models.User).where(models.User.id == id)
    user = db.execute(stmt).scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
