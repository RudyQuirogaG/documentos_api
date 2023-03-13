from fastapi import APIRouter
from ..models.user import User
from ..database.mongodb import get_database

router = APIRouter()
db = get_database()

@router.get("/users")
async def get_users():
    cursor = db.users.find()
    users = await cursor.to_list(length=100)
    return users

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    pass

@router.post("/users")
async def create_user():
    pass

@router.put("/users")
async def update_user():
    pass

@router.delete("/users")
async def delete_user():
    pass
