import os
from dotenv import load_dotenv
from fastapi import FastAPI
from .routers import users
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.get_database()

app.include_router(users.router)