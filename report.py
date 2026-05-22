from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import Reports, get_session_maker
from authentication import current_active_user
import shutil
import os
import asyncio
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

    # Save file to disk
    contents = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    # Run blocking text extraction in thread pool so server doesn't freeze
    extracted_text = await asyncio.to_thread(extract_text, file_path)

    if not extracted_text.strip():
        extracted_text = "No text could be extracted"
        status = "failed"
    else:
        status = "completed"

    new_report = Reports(
        user_id=user.id,
        original_filepath=file_path,
        extracted_text=extracted_text,
        status=status
    )

    session.add(new_report)
    await session.commit()
    await session.refresh(new_report)

    return {
        "message": "File uploaded successfully",
        "report_id": new_report.id
    }