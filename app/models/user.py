from typing import Literal
from bson import ObjectId
from pydantic import BaseModel, Field, validator, constr, EmailStr

class PyObjecId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class User(BaseModel):
    """
    Modelo para representar un usuario en el sistema.
    Campos:
        id: Identificador único del usuario.
        nombre: Nombre del usuario.
        correo_electronico: Dirección de correo electrónico del usuario.
        rol: Rol del usuario en el sistema (administrador o usuario).
        activo: Indica si el usuario está activo en el sistema.
    """

    id: PyObjecId = Field(default_factory=PyObjecId, alias='_id')
    nombre: constr(min_length=2, max_length=50) = Field(...)
    correo_electronico: EmailStr = Field(...)
    rol: Literal["administrador", "usuario"] = Field (...)
    activo: bool = Field(...)

    @validator('nombre')
    def validate_nombre(cls, v):
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError('El nombre solo puede contener letras y espacios')
        return v
    
    @validator('rol')
    def validate_rol(cls, v):
        roles_permitidos = {'administrador', 'usuario'}
        if v not in roles_permitidos:
            raise ValueError(f'Rol no permitido: {v}')
        return v
    
    class Config:
        anystr_strip_whitespace = True
        use_enum_values = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            'example': {
                'nombre': 'Juan Perez',
                'correo_electronico': 'juan.perez@example.com',
                'rol': 'usuario',
                'activo': True,
            }
        }