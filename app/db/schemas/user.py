from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

class UserOut(UserCreate):
    id: int

    class ConfigDict:
        orm_mode = True
