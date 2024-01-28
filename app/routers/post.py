from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from .. import database, models, schemas, security

router = APIRouter(prefix="/posts", tags=["posts"])


def get_current_post(id: int, db: Session = Depends(database.get_db)) -> models.Post:
    stmt = select(models.Post).where(models.Post.id == id)
    post = db.execute(stmt).scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@router.get("")
def get_posts(
    db: Session = Depends(database.get_db), limit=10, offset=0
) -> list[schemas.PostExtended]:
    """Return posts sorted by created_at."""
    subq = (
        select(*models.Post.__table__.c, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .order_by(desc(models.Post.created_at))
        .subquery()
    )
    stmt = (
        select(*subq.c, models.User.email.label("owner"))
        .join(models.User, subq.c.owner_id == models.User.id)
        .limit(limit)
        .offset(offset)
    )
    posts = db.execute(stmt).all()
    return posts


@router.get("/{id}")
def get_post(
    id: int,
    db: Session = Depends(database.get_db),
) -> schemas.PostExtended:
    subq = (
        select(*models.Post.__table__.c, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .where(models.Post.id == id)
        .group_by(models.Post.id)
        .subquery()
    )
    stmt = select(*subq.c, models.User.email.label("owner")).join(
        models.User, subq.c.owner_id == models.User.id
    )
    post = db.execute(stmt).first()
    if post is None:
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
    updated_post: schemas.PostIn,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user),
    current_post: models.Post = Depends(get_current_post),
) -> schemas.PostOut:
    if current_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    for k, v in updated_post.model_dump().items():
        current_post.__setattr__(k, v)
    db.commit()
    return current_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user),
    current_post: models.Post = Depends(get_current_post),
):
    if current_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    db.delete(current_post)
    db.commit()


def get_existing_vote(db: Session, user_id: int, post_id: int) -> models.Vote | None:
    stmt = select(models.Vote).where(
        models.Vote.user_id == user_id, models.Vote.post_id == post_id
    )
    return db.execute(stmt).scalars().first()


@router.post("/{id}/vote", status_code=status.HTTP_201_CREATED)
def vote_post(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user),
    current_post: models.Post = Depends(get_current_post),
):
    exisiting_vote = get_existing_vote(
        db, user_id=current_user.id, post_id=current_post.id
    )
    if exisiting_vote:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Already voted"
        )
    vote = models.Vote(user_id=current_user.id, post_id=current_post.id)
    db.add(vote)
    db.commit()
    return {"detail": "Vote successful"}


@router.post("/{id}/unvote")
def unvote_post(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user),
    current_post: models.Post = Depends(get_current_post),
):
    exisiting_vote = get_existing_vote(
        db, user_id=current_user.id, post_id=current_post.id
    )
    if not exisiting_vote:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Vote does not exist"
        )
    db.delete(exisiting_vote)
    db.commit()
    return {"detail": "Unvote successful"}
