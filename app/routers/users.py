from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def get_users():
    # client = get_client()
    # collection = db["users"]
    # users = []
    # async for user in collection.find():
    # db = client["ifarbo"]
    #     users.append(user)
    # return users
    pass


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
