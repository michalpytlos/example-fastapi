from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import database, models, schemas, security

router = APIRouter(tags=["auth"])


def authenticate_user(db: Session, email: str, password: str) -> models.User | None:
    stmt = select(models.User).where(models.User.email == email)
    user = db.execute(stmt).scalars().first()
    if not user:
        return None
    if not security.pwd_context.verify(secret=password, hash=user.password_hash):
        return None
    return user


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
