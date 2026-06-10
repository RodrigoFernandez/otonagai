from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ObjetivoCreate(BaseModel):
    nombre: str
    usuario_id: int


class ObjetivoUpdate(BaseModel):
    nombre: Optional[str] = None


class ObjetivoRead(BaseModel):
    id: int
    nombre: str
    imagen: Optional[str] = None
    usuario_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ObjetivoReadWithDescripciones(ObjetivoRead):
    descripciones: list["DescripcionRead"] = []  # noqa: F821

    model_config = {"from_attributes": True}


from app.schemas.descripcion import DescripcionRead  # noqa: E402, F401

ObjetivoReadWithDescripciones.model_rebuild()
