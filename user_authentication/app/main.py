from fastapi import FastAPI

from .database import Base
from .database import engine

from .routers import users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)


@app.get("/")
def home():
    return {
        "message": "Users API Running"
    }