from pydantic import BaseModel
from fastapi_users import schemas

class TextUpload(BaseModel):
    extracted_text:str
    file_type:str
    language:str
    
class UserRead(schemas.BaseUser[int]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass