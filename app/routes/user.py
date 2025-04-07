from fastapi import APIRouter
from fastapi import Path
from app.types.user import User

router = APIRouter()

@router.post("/users")
def create_user(user: User):
    return {"message": f"User {user.name} created", "data": user}

@router.get("/users/{user_id}")
def get_user(user_id: int = Path(..., title="ID of the user", gt=0, description="User ID between 1 and 1000")):
    return {"user_id": user_id}