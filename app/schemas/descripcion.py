# Esquemas Pydantic para la entidad Descripcion.
# Definen la estructura, validación y serialización de los datos
# que entran (Create) y salen (Read) de la API.
from datetime import datetime

from pydantic import BaseModel


class DescripcionCreate(BaseModel):
    # Esquema usado al crear una descripción. Todos los campos son
    # requeridos y se validan automáticamente con Pydantic.
    feria: str          # Nombre de la feria o evento
    local: str          # Nombre del local o puesto
    moneda: str         # Tipo de moneda (ARS, USD, etc.)
    precio: float       # Precio registrado
    objetivo_id: int    # ID del objetivo al que pertenece esta descripción


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
