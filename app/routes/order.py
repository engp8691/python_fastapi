from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.db.database import get_db
from app.db.models.orm_models import OrderModelDB, ProductModelDB, UserModelDB
from app.db.schemas.order import OrderCreate, OrderOut, OrderUpdate
from uuid import uuid4

from app.utils.token import get_user_in_token_data

router = APIRouter()

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", status_code=201)
async def create_order(order_data: OrderCreate, user_in_token_data = Depends(get_user_in_token_data), db: AsyncSession = Depends(get_db)):
    if (order_data.user_id != user_in_token_data["id"]):
        raise HTTPException(status_code=403, detail="Make orders for another user is forbidden")

    user_result = await db.execute(select(UserModelDB).where(UserModelDB.id == order_data.user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    product_result = await db.execute(
        select(ProductModelDB).where(ProductModelDB.id.in_(order_data.product_ids))
    )
    products = product_result.scalars().all()
    if len(products) != len(order_data.product_ids):
        raise HTTPException(status_code=400, detail="One or more products do not exist")

    order = OrderModelDB(id=uuid4().hex, name=order_data.name, price=order_data.price, user_id=order_data.user_id, products=products)
    db.add(order)
    await db.commit()
    await db.refresh(order)

    return {"order_id": order.id, "product_ids": [p.id for p in products]}

@router.get("/", response_model=List[OrderOut])
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(OrderModelDB)
        .options(
            selectinload(OrderModelDB.user),
            selectinload(OrderModelDB.products)
        )
    )
    orders = result.scalars().all()

    return orders

@router.get("/{order_id}", response_model=OrderOut)
async def get_order_details(order_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OrderModelDB)
        .where(OrderModelDB.id == order_id)
        .options(
            selectinload(OrderModelDB.user),
            selectinload(OrderModelDB.products)
        )
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order

@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: str, user_in_token_data = Depends(get_user_in_token_data), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OrderModelDB).where(OrderModelDB.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if (order.user_id != user_in_token_data["id"]):
        raise HTTPException(status_code=403, detail="Deleting orders of others is forbidden")

    await db.delete(order)
    await db.commit()
    return

@router.put("/{order_id}", response_model=OrderOut)
async def update_order(order_id: str, order_data: OrderUpdate, user_in_token_data = Depends(get_user_in_token_data), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OrderModelDB).where(OrderModelDB.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if (order.user_id != user_in_token_data["id"]):
        raise HTTPException(status_code=403, detail="Updating orders of others is forbidden")

    if order_data.name is not None:
        order.name = order_data.name

    if order_data.price is not None:
        order.price = order_data.price

    if order_data.user_id is not None:
        order.user_id = order_data.user_id

    if order_data.product_ids is not None:
        order.products.clear()

        product_result = await db.execute(
            select(ProductModelDB).where(ProductModelDB.id.in_(order_data.product_ids))
        )
        new_products = product_result.scalars().all()

        if len(new_products) != len(order_data.product_ids):
            raise HTTPException(status_code=400, detail="One or more product IDs are invalid")

        order.products = new_products

    await db.commit()

    result = await db.execute(select(OrderModelDB)
        .where(OrderModelDB.id == order_id)
        .options(
            selectinload(OrderModelDB.user),
            selectinload(OrderModelDB.products)
        )
    )
    updated_order = result.scalar_one_or_none()

    return updated_order
