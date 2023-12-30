from fastapi import FastAPI

from .routers import auth, post, user

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "hello world!"}
