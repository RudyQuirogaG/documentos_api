from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List
from ..models.documento import TipoArchivo, Archivo, Revision, Comentario, Documento
from ..database.mongodb import get_database

router = APIRouter()
db = get_database()

@router.post('/documentos')
async def create_documento(documento: Documento):
    result = await db.documento.insert_one(documento.dict())
    return {"_id": str(result.inserted_id)}

@router.get('/documentos')
async def get_documentos():
    cursor = db.documentos.find()
    documentos = await cursor.to_list(length=100)
    for documento in documentos:
        documento['_id'] = str(documento['_id'])
    return [Documento(**documento) for documento in documentos]