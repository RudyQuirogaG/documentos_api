import os
from fastapi import FastAPI
from .routers import users
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

MONGODB_URL = os.environ["MONGODB_URL"]

client = AsyncIOMotorClient(MONGODB_URL)

app.include_router(users.router)