
import bcrypt
# Monkey patch bcrypt to make it compatible with passlib 1.7.4
if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type("about", (), {})()
    bcrypt.__about__.__version__ = bcrypt.__version__

from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from typing import Optional
from sqlalchemy.future import select
from app.db.models.user import User as UserModel
from jose import jwt

# Secret key for encoding JWT
SECRET_KEY = "my-very-strong-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(email: str, password: str, db: AsyncSession):
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalars().first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    
    return user