import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

def generate_uuid_no_dash() -> str:
    return uuid.uuid4().hex  # hex gives UUID without dashes
class UserModelDB(Base):
    __tablename__ = "users"

    id = Column(String(32), primary_key=True, index=True, default=generate_uuid_no_dash)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    age = Column(Integer, nullable=False)
    hashed_password = Column(String, nullable=False, default="")
    role = Column(String, nullable=False, default="")
