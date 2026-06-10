from datetime import datetime

from pydantic import BaseModel, EmailStr


class UsuarioCreate(BaseModel):
    nombre: str
    mail: EmailStr
    password: str


class UsuarioRead(BaseModel):
    id: int
    nombre: str
    mail: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UsuarioReadSimple(BaseModel):
    id: int
    nombre: str
    mail: str

    model_config = {"from_attributes": True}
