from fastapi import APIRouter, HTTPException
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from typing import List
from ..models.categoria import Categoria
from ..database.mongodb import get_database

router = APIRouter()
db = get_database()

@router.post("/categorias")
async def create_categoria(categoria: Categoria):
    categoria_dict = jsonable_encoder(categoria)
    result = await db.categorias.insert_one(categoria_dict)
    return {"_id": str(result.inserted_id)}

@router.get("/categorias", response_model=List[Categoria])
async def get_categorias():
    cursor = db.categorias.find()
    categorias = await cursor.to_list(length=100)
    for categoria in categorias:
        categoria["_id"] = str(categoria["_id"])
    return [Categoria(**categoria) for categoria in categorias]

@router.get("/categorias/{categoria_id}")
async def get_categoria(categoria_id: str):
    categoria = await db.categorias.find_one({"_id": ObjectId(categoria_id)})
    if categoria:
        categoria["_id"] = str(categoria["_id"])
        categoria = Categoria(**categoria)
        return categoria
    else:
        raise HTTPException(status_code=404, detail="Categoria not found")

@router.put("/categorias/{categoria_id}")
async def update_categoria(categoria_id: str, categoria: Categoria):
    result = await db.categorias.update_one({"_id": ObjectId(categoria_id)}, {"$set": categoria.dict()})
    if result.matched_count:
        return{"message": "Categoria update succesfully"}
    else:
        raise HTTPException(status_code=404, detail="Categoria no found")

@router.delete("/categorias/{categoria_id}")
async def delete_categoria(categoria_id: str):
    result = await db.categorias.delete_one({"_id": ObjectId(categoria_id)})
    if result.deleted_count:
        return {"message": "Categoria deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Categoria not found")
    