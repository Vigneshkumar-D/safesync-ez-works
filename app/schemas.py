from pydantic import BaseModel, EmailStr
from typing import List
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "Ops"

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class FileUpload(BaseModel):
    filename: str

class FileResponse(BaseModel):
    id: int
    filename: str
    secure_url: str

    class Config:
        orm_mode = True
