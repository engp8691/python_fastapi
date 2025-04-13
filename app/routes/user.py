import bcrypt

from app.types.user import LoginPayload
# Monkey patch bcrypt to make it compatible with passlib 1.7.4
if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type("about", (), {})()
    bcrypt.__about__.__version__ = bcrypt.__version__

from fastapi import APIRouter, HTTPException, Path, Depends, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.schemas.user import UserCreate, UserOut, UserUpdate
from app.db.database import get_db
from app.db.models.user import UserModelDB
from app.utils.token import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user, hash_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

# route to create a user
@router.post("/users", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(select(UserModelDB).where(UserModelDB.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    user_dict = user.model_dump()
    user_dict.pop("password")  # remove plain password
    user_dict["hashed_password"] = hash_password(user.password)  # add hashed password
    new_user = UserModelDB(**user_dict)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return UserOut.model_validate(new_user)
    # return new_user

# route to retrieve all users
@router.get("/users")
async def get_users(
    current_user: UserModelDB = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=10, ge=1, le=100),
    page: int = Query(default=0, ge=0),
):
    if (current_user.role != "administrator"):
        raise HTTPException(status_code=403, detail=f"{current_user.name} have no admistrator permission to get all users!")

    result = await db.execute(
        select(UserModelDB).limit(limit).offset(page)
    )
    users = result.scalars().all()

    return [UserOut.model_validate(user) for user in users]

# route to retrieve a user
@router.get("/users/{user_id}")
async def get_user(db: AsyncSession = Depends(get_db), user_id: str = Path(..., title="ID of the user", min_length=32, max_length=32)):
    result = await db.execute(select(UserModelDB).where(UserModelDB.id == user_id))
    existing_user = result.scalars().first()
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User with id={user_id} does not exist")

    return UserOut.model_validate(existing_user)
    # return existing_user

# route to remove a user
@router.delete("/users/{user_id}")
async def delete_user(db: AsyncSession = Depends(get_db), user_id: str = Path(..., title="ID of the user", min_length=32, max_length=32)):
    # Fetch the user by ID
    result = await db.execute(select(UserModelDB).where(UserModelDB.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete user
    await db.delete(user)
    await db.commit()

    return {"message": f"User with id={user_id} deleted."}

# route to update a user
@router.put("/users/{user_id}")
async def update_user(user_update: UserUpdate, user_id: str = Path(..., title="ID of the user", min_length=32, max_length=32), db: AsyncSession = Depends(get_db),):
    # Fetch the user by ID
    result = await db.execute(select(UserModelDB).where(UserModelDB.id == user_id))
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
    if user_update.role is not None:
        user.role = user_update.role
    if user_update.password is not None:
        user.hashed_password = hash_password(user_update.password)
    
    await db.commit()
    await db.refresh(user)

    return {"message": "User updated", "user": UserOut.model_validate(user)}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "user": {
                "name": user.name,
                "role": user.role,
                "age": user.age,
                "email": user.email
            }
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/v2/login")
async def login(payload: LoginPayload, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(payload.email, payload.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "user": {
                "name": user.name,
                "role": user.role,
                "age": user.age,
                "email": user.email
            }
        },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
