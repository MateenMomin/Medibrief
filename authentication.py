from typing import Optional
from fastapi import Depends,Request
from fastapi_users import BaseUserManager,FastAPIUsers,models,IntegerIDMixin
from fastapi_users.authentication import(
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy
)
from fastapi_users.db import SQLAlchemyUserDatabase
import os
from db import User,get_user_db
from dotenv import load_dotenv
load_dotenv()
SECRET=os.getenv("SECRET")
if not SECRET:
    raise ValueError("Enviroment variable not set ")

class User_Manager(IntegerIDMixin,BaseUserManager[User,int]):
    reset_password_token_secret=os.getenv("SECRET")
    verification_token_secret=os.getenv("SECRET")
    
    async def on_after_register(self, user, request = None):
        print(f"User {user.id} has registered")
    async def on_after_forgot_password(self, user, token, request = None):
        print(f"User {user.id} has forgotten the password.Reset Password={token}")
    async def on_after_request_verify(self, user, token, request = None):
        print(f"Verification Requested for user {user.id}.Verification Token={token}")
    
async def get_user_manager(user_db:SQLAlchemyUserDatabase=Depends(get_user_db)):
    yield User_Manager(user_db)

bearer_transport=BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy():
    return JWTStrategy(secret=os.getenv("SECRET"),lifetime_seconds=3600)

auth_backend=AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)
fastapi_user=FastAPIUsers[User,int](get_user_manager,auth_backends=[auth_backend])
current_active_user=fastapi_user.current_user(active=True)