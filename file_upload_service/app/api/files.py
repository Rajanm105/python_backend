from fastapi import APIRouter, UploadFile, File

from app.services.file_services import save_file
from app.utils.validators import validate_extension

router = APIRouter(tags=["Files"])


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):
    validate_extension(file.filename)

    uploaded_file = save_file(file)

    return {
        "message": "File uploaded successfully.",
        "file": uploaded_file
    }