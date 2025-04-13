
import bcrypt
# Monkey patch bcrypt to make it compatible with passlib 1.7.4
if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type("about", (), {})()
    bcrypt.__about__.__version__ = bcrypt.__version__

from fastapi import Depends, HTTPException
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from typing import Optional
from sqlalchemy.future import select
from app.db.models.user import UserModelDB
from app.db.database import get_db

# Secret key for encoding JWT
SECRET_KEY = "my-very-strong-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(email: str, password: str, db: AsyncSession) -> UserModelDB:
    result = await db.execute(select(UserModelDB).where(UserModelDB.email == email))
    user = result.scalars().first()

    if not user or not verify_password(password, user.hashed_password):
        return False
    
    return user

async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_data = payload.get("user")
        if user_data is None:
            raise credentials_exception
        
        # userObj = UserUpdate(**user_data)
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials 1234")

    # result = await db.execute(select(UserModelDB).where(UserModelDB.email == userObj.email))
    result = await db.execute(select(UserModelDB).where(UserModelDB.email == user_data["email"]))
    user = result.scalars().first()

    if user is None:
        raise credentials_exception

    return user

def hash_password(password: str) -> str:
    return pwd_context.hash(password)