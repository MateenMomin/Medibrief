from fastapi import FastAPI,HTTPException,Depends,UploadFile,File,Query
from db import User,Reports,get_session_maker,create_tables_and_all,Reports
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from schema import TextUpload,UserRead,UserCreate,UserUpdate
from authentication import current_active_user,fastapi_user,auth_backend
import shutil
import os
from report import router as file_router
from sqlalchemy import select
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from report_router import router as report_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_tables_and_all()
    yield


app=FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 
 
app.include_router(
    fastapi_user.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"])

app.include_router(
    fastapi_user.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(file_router)
app.include_router(report_router)


@app.post("/reports")
async def Text_Upload(
    data:TextUpload,
    session:AsyncSession=Depends(get_session_maker),
    user=Depends(current_active_user)):
    
    new_report=Reports(
        extracted_text=data.extracted_text,
        user_id=user.id,
        language=data.language
    )
    session.add(new_report)
    await session.commit()
    await session.refresh(new_report)
    
    return {"message":"Report saved successfully",
            "report_id":new_report.id}
    

@app.get("/reports")
async def get_reports(
    report_id: Optional[int] = Query(default=None),
    session: AsyncSession = Depends(get_session_maker),
    user=Depends(current_active_user)
):
    
    if report_id is not None:
        result = await session.execute(
            select(Reports).where(
                Reports.id == report_id
            )
        )
        report = result.scalar_one_or_none()

        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        if report.user_id!=user.id:
            raise HTTPException(status_code=403,detail="Report does Not Belong to you")

        return report


    result = await session.execute(
        select(Reports).where(Reports.user_id == user.id)
    )
    reports = result.scalars().all()

    return reports
    
