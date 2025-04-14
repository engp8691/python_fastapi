# app/schemas/order.py
from pydantic import BaseModel, Field
from typing import List, Optional

from app.db.schemas.product import ProductOut
from app.db.schemas.user import UserOut

class OrderCreate(BaseModel):
    name: str
    price: float
    user_id: str
    product_ids: List[str]

class OrderUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    user_id: Optional[str] = None
    product_ids: Optional[List[str]] = Field(default=None, description="List of product IDs")

class OrderOut(BaseModel):
    id: str
    name: str
    price: float
    user: UserOut
    products: List[ProductOut]

    class Config:
        from_attributes = True
