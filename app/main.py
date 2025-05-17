from fastapi import FastAPI

from .log import setup_logging
from .routers import auth, post, user

setup_logging()

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "hello world!"}
