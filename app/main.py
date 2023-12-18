from fastapi import FastAPI

from . import database, models
from .routers import auth, post, user

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

models.Base.metadata.create_all(bind=database.engine)


@app.get("/")
async def root():
    return {"message": "hello world!"}
