# Esquemas Pydantic para la entidad Descripcion.
# Definen la estructura, validación y serialización de los datos
# que entran (Create) y salen (Read) de la API.
from datetime import datetime

from pydantic import BaseModel, Field


class DescripcionCreate(BaseModel):
    feria: str
    local: str
    moneda: str
    precio: float = Field(gt=0)
    objetivo_id: int


class DescripcionRead(BaseModel):
    # Esquema usado al devolver una descripción en las respuestas.
    # Incluye el id y created_at generados por la base de datos.
    # from_attributes=True permite mapear desde un modelo SQLAlchemy.
    id: int
    feria: str
    local: str
    moneda: str
    precio: float
    objetivo_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
