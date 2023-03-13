from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, validator, constr

class ObjectIdStr(str):
    """Clase personalizada para serializar/deserializar ObjecId"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("No es un ObjectId valido")
        return str(v)

class User(BaseModel):
    id: Optional[ObjectId] = Field(alias='_id', default=None)
    nombre: constr(min_length=2, max_length=50) = Field(...)
    correo_electronico: str = Field(...)
    rol: constr(regex='^(administrador|usuarios)$') = Field (...)
    activo: bool = Field(...)

    @validator('nombre')
    def validate_nombre(cls, v):
        if not v:
            raise ValueError('No puede estar vacio')
        return v

    # @validator('correo_electronico')
    # def validate_correo_electronico(cls, v):
    #     if not Email.validate(v):
    #         raise ValueError('No es una direccion de correo electronico valida.')
    #     return v
    
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