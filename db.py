from collections.abc import AsyncGenerator
from sqlalchemy import String,Column,Text,DateTime,ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase,relationship
from sqlalchemy import Integer,VARCHAR
from datetime import datetime
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase,SQLAlchemyBaseUserTable

class Base(DeclarativeBase):
    pass

DATABASE_URL="mysql+aiomysql://root:mateen7840@127.0.0.1:3306/medibrief"

class User(SQLAlchemyBaseUserTable[int],Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True,nullable=False)
    reports = relationship("Reports", back_populates="user",cascade="all, delete")

class Reports(Base):
    __tablename__="reports"
    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    original_filepath=Column(VARCHAR(255))
    extracted_text=Column(Text)
    summarized_text=Column(Text)
    language=Column(VARCHAR(255))
    created_at=Column(DateTime,default=datetime.utcnow)
    user = relationship("User", back_populates="reports")

engine=create_async_engine(DATABASE_URL)
async_session_maker=async_sessionmaker(engine,expire_on_commit=False)

async def create_tables_and_all():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def get_session_maker()->AsyncGenerator[AsyncSession,None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session:AsyncSession=Depends(get_session_maker)):
    yield SQLAlchemyUserDatabase(session,User)