import os
from dotenv import load_dotenv
from fastapi import FastAPI
from .routers import users
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()
app = FastAPI()

MONGODB_URI = os.environ["MONGODB_URI"]

client = AsyncIOMotorClient(MONGODB_URI)

app.include_router(users.router)