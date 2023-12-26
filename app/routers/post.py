from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from .. import database, models, schemas, security

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("")
def get_posts(db: Session = Depends(database.get_db)) -> list[schemas.Post]:
    stmt = select(models.Post)
    posts = db.execute(stmt).scalars().all()
    return posts


@router.get("/{id}")
def get_post(id: int, db: Session = Depends(database.get_db)) -> schemas.Post:
    stmt = select(models.Post).where(models.Post.id == id)
    post = db.execute(stmt).scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(
    post: schemas.BasePost,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user),
) -> schemas.Post:
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{id}")
def update_post(
    id: int,
    updated_post: schemas.BasePost,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user),
) -> schemas.Post:
    stmt = (
        update(models.Post)
        .where(models.Post.id == id)
        .values(**updated_post.model_dump())
    )
    result = db.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    db.commit()
    stmt = select(models.Post).where(models.Post.id == id)
    return db.execute(stmt).scalars().first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    stmt = delete(models.Post).where(models.Post.id == id)
    result = db.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    db.commit()
