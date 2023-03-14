from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List
from ..models.categoria import Categoria
from ..database.mongodb import get_database

router = APIRouter()
db = get_database()

@router.post("/categorias")
async def create_categoria(categoria: Categoria):
    result = await db.categorias.insert_one(categoria.dict())
    return {"_id": str(result.inserted_id)}

@router.get("/categorias", response_model=List[Categoria])
async def get_categorias():
    cursor = db.categorias.find()
    categorias = await cursor.to_list(length=100)
    for categoria in categorias:
        categoria["_id"] = str(categoria["_id"])
    return [Categoria(**categoria) for categoria in categorias]