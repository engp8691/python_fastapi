from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0, lt=120)
    email: str
    userid: Optional[int] = Field(default=None, gt=100, lt=1000)
