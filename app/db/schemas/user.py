from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, create_model

class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: int = Field(..., ge=0)
    role: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    password: Optional[str] = None
    role: Optional[str] = None