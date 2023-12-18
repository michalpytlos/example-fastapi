from fastapi import FastAPI

from . import database, models
from .routers import post

app = FastAPI()

app.include_router(post.router)

models.Base.metadata.create_all(bind=database.engine)


@app.get("/")
async def root():
    return {"message": "hello world!"}
