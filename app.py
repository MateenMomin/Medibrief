from fastapi import FastAPI,HTTPException,Depends,UploadFile,File,Query
from db import User,Reports,get_session_maker,create_tables_and_all,Reports
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from authentication import current_active_user,fastapi_user,auth_backend
import shutil
import os
from report import router as file_router
from fastapi.middleware.cors import CORSMiddleware
from report_router import router as report_router
from schema import UserRead, UserCreate

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

    
