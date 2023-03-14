from typing import Literal
from bson import ObjectId
from ..utils import PyObjecId
from pydantic import BaseModel, EmailStr, Field, validator, constr

class Categoria(BaseModel):
    """
    Modelo para representar las categorias en el sistema.
    Campos:
        id: Identificador único de categoria.
        nombre: Nombre de categoria (Contrato o Carta).
        descripcion: Una descripcion de la categoria.
        activo: Indica si el usuario está activo en el sistema.
    """
    id: PyObjecId = Field(default_factory=PyObjecId, alias='_id')
    nombre: constr(min_length=2, max_length=50) = Field(...)
    descripcion: constr(min_length=2, max_length=200) = Field(...)
    activo: bool = Field(...)

    @validator('nombre')
    def nombre_alpha_spaces(cls, v):
        """
        Verifica que el nombre solo contenga caracteres alfanuméricos y espacios en blanco.
        """
        if not v.replace(' ', '').isalnum():
            raise ValueError('El nombre solo puede contener caracteres alfanumericos y espacios en blanco')
        else:
            return v
        
    @validator('activo')
    def activo_bool(cls, v):
        """
        Verifica que el valor de "activo" sea un valor booleano.
        """
        if not isinstance(v, bool):
            raise ValueError('El valor de "activo" debe ser True o False')
        return v

    class Config:
        anystr_strip_whitespace = True
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        schema_extra = {
            'example': {
                'nombre': 'Contratos',
                'descripcion': 'Documentos legales que establecen acuerdos entre la empresa y sus clientes o proveedores',
                'activo': True,
            }
        }