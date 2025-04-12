from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from pydantic import BaseModel, field_validator
import re

class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0, lt=120)
    email: str
    role: str
    hashed_password: str
    userid: Optional[int] = Field(default=None, gt=100, lt=1000)

class LoginPayload(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value):
        if len(value) < 9:
            raise ValueError("Password must be at least 9 characters long")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", value):
            raise ValueError("Password must contain at least one special character")
        return value