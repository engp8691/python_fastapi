from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db  # your DB session dependency
from app.db.models.user import ProductModelDB
from app.db.schemas.product import ProductCreate, ProductOut, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductOut)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    new_product = ProductModelDB(**product.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


@router.get("/", response_model=list[ProductOut])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProductModelDB))
    return result.scalars().all()


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: str = Path(..., title="ID of the user", min_length=32, max_length=32), db: AsyncSession = Depends(get_db)):
    print(9999930, product_id)
    result = await db.execute(select(ProductModelDB).where(ProductModelDB.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductOut)
async def update_product(product_update: ProductUpdate, product_id: str = Path(..., title="ID of the user", min_length=32, max_length=32), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProductModelDB).where(ProductModelDB.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    await db.commit()
    await db.refresh(product)
    return product


@router.delete("/{product_id}")
async def delete_product(product_id: str = Path(..., title="ID of the user", min_length=32, max_length=32), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProductModelDB).where(ProductModelDB.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)
    await db.commit()
    return {"detail": "Product deleted"}
