# app/schemas/order.py
from pydantic import BaseModel
from typing import List

class OrderCreate(BaseModel):
    name: str
    price: float
    user_id: str
    product_ids: List[str]


class OrderOut(BaseModel):
    id: str
    user_id: str
    product_ids: List[str]
    total_amount: float

    class Config:
        from_attributes = True
