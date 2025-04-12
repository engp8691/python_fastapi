from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: int = Field(..., ge=0)
    role: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    hashed_password: Optional[str] = None

    class ConfigDict:
        orm_mode = True
