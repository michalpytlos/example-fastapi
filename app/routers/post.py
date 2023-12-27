from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import database, models, schemas, security

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("")
def get_posts(
    db: Session = Depends(database.get_db), limit=10, offset=0
) -> list[schemas.PostOut]:
    stmt = select(models.Post).limit(limit).offset(offset)
    posts = db.execute(stmt).scalars().all()
    return posts


@router.get("/{id}")
def get_post(id: int, db: Session = Depends(database.get_db)) -> schemas.PostOut:
    stmt = select(models.Post).where(models.Post.id == id)
    post = db.execute(stmt).scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(
    post: schemas.PostIn,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user),
) -> schemas.PostOut:
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{id}")
def update_post(
    id: int,
    updated_post: schemas.PostIn,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user),
) -> schemas.PostOut:
    stmt = select(models.Post).where(models.Post.id == id)
    post = db.execute(stmt).scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    for k, v in updated_post.model_dump().items():
        post.__setattr__(k, v)
    db.commit()
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    stmt = select(models.Post).where(models.Post.id == id)
    post = db.execute(stmt).scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    db.delete(post)
    db.commit()
