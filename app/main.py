from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import ALLOWED_ORIGINS
from app.middlewares.log import LogMiddleware as logger
from app.routes import hello, user, product, order
from app.routes import rpc
from app.grpc.grpc_server import start_grpc_server
import asyncio

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom logger middleware
app.add_middleware(logger)

# Include all routes
app.include_router(hello.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(rpc.router)

# 🚀 Launch gRPC server alongside FastAPI
@app.on_event("startup")
async def launch_grpc():
    asyncio.create_task(start_grpc_server())
