# app/routes/order.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.db.models.orm_models import OrderModelDB, ProductModelDB, UserModelDB
from app.db.schemas.order import OrderCreate
from uuid import uuid4

router = APIRouter()

@router.post("/orders", status_code=201)
async def create_order(order_data: OrderCreate, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    user_result = await db.execute(select(UserModelDB).where(UserModelDB.id == order_data.user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if products exist
    product_result = await db.execute(
        select(ProductModelDB).where(ProductModelDB.id.in_(order_data.product_ids))
    )
    products = product_result.scalars().all()
    if len(products) != len(order_data.product_ids):
        raise HTTPException(status_code=400, detail="One or more products not found")

    # Create order
    order = OrderModelDB(id=uuid4().hex, name=order_data.name, price=order_data.price, user_id=order_data.user_id, products=products)
    db.add(order)
    await db.commit()
    await db.refresh(order)

    return {"order_id": order.id, "product_ids": [p.id for p in products]}
