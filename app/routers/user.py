from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import database, models, schemas, security

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserIn, db: Session = Depends(database.get_db)):
    password_hash = security.pwd_context.hash(user.password)
    new_user = models.User(email=user.email, password_hash=password_hash)
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="User with this email already exists."
        )
    db.refresh(new_user)
    return new_user


@router.get("/me", response_model=schemas.UserOut)
def get_user_me(
    current_user: models.User = Depends(security.get_current_user),
):
    return current_user


@router.get("", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(database.get_db)):
    stmt = select(models.User)
    return db.execute(stmt).scalars().all()
