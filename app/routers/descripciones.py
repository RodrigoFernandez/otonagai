from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.descripcion import DescripcionCreate, DescripcionRead
from app.services.descripcion import DescripcionService

router = APIRouter(prefix="/api/descripciones", tags=["descripciones"])


@router.post("/", response_model=DescripcionRead, status_code=status.HTTP_201_CREATED)
async def crear_descripcion(data: DescripcionCreate, db: AsyncSession = Depends(get_db)):
    service = DescripcionService(db)
    return await service.create(data)


@router.get("/{descripcion_id}", response_model=DescripcionRead)
async def obtener_descripcion(
    descripcion_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = DescripcionService(db)
    return await service.get_by_id(descripcion_id)


@router.delete("/{descripcion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_descripcion(
    descripcion_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = DescripcionService(db)
    await service.delete(descripcion_id)
