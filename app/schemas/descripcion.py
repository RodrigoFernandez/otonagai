from datetime import datetime

from pydantic import BaseModel


class DescripcionCreate(BaseModel):
    feria: str
    local: str
    moneda: str
    precio: float
    objetivo_id: int


class DescripcionRead(BaseModel):
    id: int
    feria: str
    local: str
    moneda: str
    precio: float
    objetivo_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
