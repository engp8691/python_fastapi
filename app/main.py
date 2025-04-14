from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import ALLOWED_ORIGINS
from app.middlewares.log import LogMiddleware as logger
from app.routes import hello, user, product, order

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(logger)

# Include routes from hello.py
app.include_router(hello.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(order.router)