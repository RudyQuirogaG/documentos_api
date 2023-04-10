from fastapi import APIRouter, HTTPException
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from ..models.documento import Documento
from ..database.mongodb import get_database

router = APIRouter()
db = get_database()

@router.post('/documentos')
async def create_documento(documento: Documento):
    categoria = await db['categorias'].find({'_id': ObjectId(documento.id_categoria)}).limit(1).to_list(length=1)
    if categoria is None:
        raise HTTPException(status_code=404, detail='Categoria no encontrada')
    documento_dict = jsonable_encoder(documento)
    result = await db.documentos.insert_one(documento_dict)
    return {"_id": str(result.inserted_id)}

@router.get('/documentos')
async def get_documentos():
    cursor = db.documentos.find()
    documentos = await cursor.to_list(length=100)
    for documento in documentos:
        documento['_id'] = str(documento['_id'])
    return [Documento(**documento) for documento in documentos]

@router.get('/documentos/{documento_id}')
async def get_documento(documento_id: str):
    documento = await db.documentos.find({'_id': ObjectId(documento_id)}).limit(1).to_list(length=1)
    if documento:
        documento['_id'] = str(documento['_id'])
        documento = Documento(**documento)
        return documento
    else:
        raise HTTPException(status_code=404, detail='Documento no encontrado')
    
@router.put('/documentos/{documento_id}')
async def update_documento(documento_id: str, documento: Documento):
    result = await db.documentos.update_one({'_id': ObjectId(documento_id)}, {'$set': documento.dict()})
    if result.matched_count:
        return{'message': 'Documento actualizado correctamente'}
    else:
        raise HTTPException(status_code=404, detail='Documento no encontrado')
    
@router.delete('/documentos/{documento_id}')
async def delete_documento(documento_id: str):
    result = await db.documentos.delete_one({'_id': ObjectId(documento_id)})    
    if result.deleted_count:
        return {'message': 'Documento eleminado correctamente'}
    else:
        raise HTTPException(status_code=404, detail='Documento no encontrado.')