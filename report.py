from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import Reports, get_session_maker
from authentication import current_active_user
import shutil
import os
from textextractor import extract_text

router = APIRouter(prefix="/files", tags=["files"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session_maker),
    user=Depends(current_active_user),
):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    extracted_text = extract_text(file_path)

    new_report = Reports(
        user_id=user.id,
        original_filepath=file_path,
    )

    session.add(new_report)
    await session.commit()
    await session.refresh(new_report)

    return {
        "message": "File uploaded successfully",
        "report_id": new_report.id
    }


