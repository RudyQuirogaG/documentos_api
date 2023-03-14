from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List
from ..models.user import User
from ..database.mongodb import get_database

router = APIRouter()
db = get_database()

@router.get("/users", response_model=List[User])
async def get_users():
    cursor = db.users.find()
    users = await cursor.to_list(length=100)
    for user in users:
        user["_id"] = str(user["_id"])
    return [User(**user) for user in users]

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/users")
async def create_user(user: User):
    result = await db.users.insert_one(user.dict())
    return {"_id": str(result.inserted_id)}

@router.put("/users")
async def update_user():
    pass

@router.delete("/users")
async def delete_user():
    pass
