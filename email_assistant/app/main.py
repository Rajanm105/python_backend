from fastapi import FastAPI

from .database import Base, engine
from .routers import emails

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Email Reply Assistant API")

app.include_router(emails.router)


@app.get("/")
def root():
    return {"message": "AI Email Reply Assistant API is running"}