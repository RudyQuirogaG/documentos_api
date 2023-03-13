from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, Email, validator, constr

class User(BaseModel):
    id: Optional[ObjectId] = Field(alias='_id')
    nombre: constr(min_length=2, max_length=50) = Field(...)
    correo_electronico: str = Field(...)
    rol: constr(regex='^(administrador|usuarios)$') = Field (...)
    activo: bool = Field(...)

    @validator('nombre')
    def validate_nombre(cls, v):
        if not v:
            raise ValueError('No puede estar vacio')
        return v

    @validator('correo_electronico')
    def validate_correo_electronico(cls, v):
        if not Email.validate(v):
            raise ValueError('No es una direccion de correo electronico valida.')
        return v
    
    @validator('rol')
    def validate_rol(cls, v):
        roles_permitidos = {'administrador', 'usuario'}
        if v not in roles_permitidos:
            raise ValueError(f'Rol no permitido: {v}')
        return v