import uuid
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from app.db.models.base import Base

def generate_uuid_no_dash() -> str:
    return uuid.uuid4().hex  # hex gives UUID without dashes

order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", String(32), ForeignKey("orders.id"), primary_key=True),
    Column("product_id", String(32), ForeignKey("products.id"), primary_key=True),
)
class UserModelDB(Base):
    __tablename__ = "users"

    id = Column(String(32), primary_key=True, index=True, default=lambda: uuid.uuid4().hex)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    age = Column(Integer, nullable=False)
    hashed_password = Column(String, nullable=False, default="")
    role = Column(String, nullable=False, default="")

    orders = relationship("OrderModelDB", back_populates="user", cascade="all, delete-orphan")

class OrderModelDB(Base):
    __tablename__ = "orders"

    id = Column(String(32), primary_key=True, index=True, default=lambda: uuid.uuid4().hex)
    item = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    user_id = Column(String(32), ForeignKey("users.id"), nullable=False)

    user = relationship("UserModelDB", back_populates="orders")
    products = relationship("ProductModelDB", secondary=order_product, back_populates="orders")


class ProductModelDB(Base):
    __tablename__ = "products"

    id = Column(String(32), primary_key=True, index=True, default=lambda: uuid.uuid4().hex)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    orders = relationship("OrderModelDB", secondary=order_product, back_populates="products")


