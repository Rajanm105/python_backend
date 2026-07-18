from fastapi import FastAPI

from app.api.files import router as file_router
app = FastAPI(
    title="File upload"
)

app.include_router(file_router)

