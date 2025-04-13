from fastapi import FastAPI
from app.routes import hello, user, product, order

app = FastAPI()

# Include routes from hello.py
app.include_router(hello.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(order.router)