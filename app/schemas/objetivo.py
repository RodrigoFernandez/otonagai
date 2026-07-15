# Esquemas Pydantic para la entidad Objetivo.
# Incluyen Create (creación), Update (modificación parcial) y
# dos variantes de Read: una simple y otra con descripciones anidadas.
# El orden de definición requiere un import diferido y model_rebuild()
# para resolver la referencia circular con DescripcionRead.
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ObjetivoCreate(BaseModel):
    # Esquema usado al crear un objetivo.
    nombre: str
    usuario_id: int


class ObjetivoUpdate(BaseModel):
    # Esquema usado al actualizar un objetivo.
    # Todos los campos son opcionales (Partial Update / PATCH).
    nombre: Optional[str] = None


class ObjetivoRead(BaseModel):
    # Esquema base de respuesta para un objetivo.
    # Incluye la URL de la imagen si existe.
    id: int
    nombre: str
    imagen: Optional[str] = None   # URL relativa de la imagen subida
    usuario_id: int
    created_at: datetime

    model_config = {"from_attributes": True}



