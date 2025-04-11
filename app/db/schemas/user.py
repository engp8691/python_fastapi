from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    hashed_password: Optional[str] = None
    role: str

class UserOut(UserCreate):
    id: int

    class ConfigDict:
        orm_mode = True
