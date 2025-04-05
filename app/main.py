from fastapi import FastAPI
from app.routes import hello

app = FastAPI()

# Include routes from hello.py
app.include_router(hello.router)
