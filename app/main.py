from fastapi import FastAPI, status, HTTPException

from . import schemas

app = FastAPI()


posts_db: dict[int, schemas.Post] = {}


@app.get("/")
async def root():
    return {"message": "hello world!"}


@app.get("/posts")
def get_posts() -> list[schemas.Post]:
    return [post for post in posts_db.values()]


@app.get("/posts/{id}")
def get_post(id: int) -> schemas.Post:
    if id not in posts_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return posts_db[id]


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post) -> schemas.Post:
    posts_db[post.id] = post
    return post


@app.put("/posts/{id}")
def update_post(id: int, post: schemas.Post) -> schemas.Post:
    if id not in posts_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    posts_db[id] = post
    return posts_db[id]


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    if id not in posts_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    posts_db.pop(id)
