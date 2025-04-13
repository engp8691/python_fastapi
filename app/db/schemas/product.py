from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    name: str
    price: float

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]

class ProductOut(ProductBase):
    id: str

    class Config:
        from_attributes = True
