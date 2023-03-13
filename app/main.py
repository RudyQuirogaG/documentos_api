from fastapi import FastAPI
from .routers import users
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

app.include_router(users.router)