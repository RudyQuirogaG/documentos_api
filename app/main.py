from fastapi import FastAPI
from .routers import users, categorias
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

app.include_router(users.router)
app.include_router(categorias.router)