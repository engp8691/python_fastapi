from fastapi import APIRouter, HTTPException, Path, Depends
from app.types.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.schemas.user import UserCreate, UserOut
from app.db.database import get_db
from app.db.models.user import User as UserModel

router = APIRouter()
users = []

# route to create a user
@router.post("/users", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(select(UserModel).where(UserModel.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = UserModel(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

# route to retrieve all users
@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel))
    users = result.scalars().all()
    return users

# route to retrieve a user
@router.get("/users/{user_id}")
async def get_user(db: AsyncSession = Depends(get_db), user_id: int = Path(..., title="ID of the user", gt=0, description="User ID between 1 and 1000")):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    existing_user = result.scalars().first()
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User with id={user_id} does not exist")

    return existing_user

# route to remove a user
@router.delete("/users/{user_id}")
async def delete_user(db: AsyncSession = Depends(get_db), user_id: int = Path(..., title="ID of the user", gt=0, description="User ID between 1 and 1000")):
    # Fetch the user by ID
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete user
    await db.delete(user)
    await db.commit()

    return {"message": f"User with id={user_id} deleted."}

# route to update a user
@router.put("/users/{user_id}")
async def update_user(user_update: UserCreate, user_id: int = Path(..., title="ID of the user", gt=0, description="User ID between 1 and 1000"), db: AsyncSession = Depends(get_db),):
    # Fetch the user by ID
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user
    if user_update.name is not None:
        user.name = user_update.name
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.age is not None:
        user.age = user_update.age

    await db.commit()
    await db.refresh(user)

    return {"message": "User updated", "user": user}
