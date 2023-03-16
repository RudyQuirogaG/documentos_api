from typing import Optional, List
from enum import Enum
from bson import ObjectId
from datetime import datetime
from ..utils import PyObjectId
from pydantic import BaseModel, Field, validator, constr, root_validator

class TipoArchivo(Enum):
    PDF = 'pdf'
    DOCX = 'docx'
    XLSX = 'xlsx'
    JPG = 'jpg'
    PNG = 'png'

class Archivo(BaseModel):
    nombre: str = Field(...)
    tipo: TipoArchivo = Field(...)
    tamaño: Optional[str] = Field(default=None)
    url: Optional[str] = Field(default=None)

    class Config:
        anystr_strip_whitespace = True


class Revision(BaseModel):
    numero: int = Field(...)
    fecha: datetime = Field(default_factory=datetime)
    responsable: PyObjectId = Field(...)
    comentarios: Optional[str] = Field(default=None)

    @validator('numero')
    def validate_numero(cls, v):
        if v < 0:
            raise ValueError('El numero de la revision no puede ser negativo')
        return v
    
    class Config:
        anystr_strip_whitespace = True
        json_encoders = {ObjectId: str}

class Comentario(BaseModel):
    usuario: PyObjectId = Field(...)
    fecha: datetime = Field(default_factory=datetime)
    texto: Optional[str] = Field(default=None)

    class Config:
        anystr_strip_whitespace = True
        json_encoders = {ObjectId: str}

class Documento(BaseModel):
    """
    Modelo para representar un documento en el sistema.
    Campos:

    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    titulo: constr(min_length=2, max_length=50) = Field(...)
    descripcion: constr(min_length=2, max_length=200) = Field(...)
    categoria_id: PyObjectId
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_modificacion: datetime = Field(default_factory=datetime.utcnow)
    creado_por: PyObjectId
    modificado_por: PyObjectId
    archivos: List[Archivo]
    revisiones: List[Revision]
    comentarios: List[Comentario]

    @root_validator
    def check_fechas(cls, values):
        if values['fecha_modificacion'] < values['fecha_creacion']:
            raise ValueError('La fecha de modificacion debe ser posterior o igual a fecha de creación')
        return values

    @validator('fecha_creacion', pre= True, always=True)
    def parse_fecha_creacion(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v)
        return v
    
    @validator('fecha_creacion', pre=False, always=True)
    def format_fecha_creacion(cls, v):
        return v.isoformat()
    
    class Config:
        anystr_strip_whitespace = True
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True