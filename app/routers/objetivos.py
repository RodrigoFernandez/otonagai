from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.descripcion import DescripcionRead
from app.schemas.objetivo import ObjetivoCreate, ObjetivoRead, ObjetivoUpdate
from app.services.descripcion import DescripcionService
from app.services.objetivo import ObjetivoService

router = APIRouter(prefix="/api/objetivos", tags=["objetivos"])


@router.post("/", response_model=ObjetivoRead, status_code=status.HTTP_201_CREATED)
async def crear_objetivo(data: ObjetivoCreate, db: AsyncSession = Depends(get_db)):
    service = ObjetivoService(db)
    return await service.create(data)


@router.get("/{objetivo_id}", response_model=ObjetivoRead)
async def obtener_objetivo(objetivo_id: int, db: AsyncSession = Depends(get_db)):
    service = ObjetivoService(db)
    return await service.get_by_id(objetivo_id)


@router.get("/", response_model=list[ObjetivoRead])
async def listar_objetivos(
    usuario_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    service = ObjetivoService(db)
    return await service.list_by_usuario(usuario_id)


@router.put("/{objetivo_id}", response_model=ObjetivoRead)
async def actualizar_objetivo(
    objetivo_id: int,
    data: ObjetivoUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = ObjetivoService(db)
    return await service.update(objetivo_id, data)


@router.delete("/{objetivo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_objetivo(objetivo_id: int, db: AsyncSession = Depends(get_db)):
    service = ObjetivoService(db)
    await service.delete(objetivo_id)


@router.post("/{objetivo_id}/imagen", response_model=ObjetivoRead)
async def subir_imagen_objetivo(
    objetivo_id: int,
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
):
    service = ObjetivoService(db)
    return await service.upload_image(objetivo_id, file)


@router.get("/{objetivo_id}/descripciones", response_model=list[DescripcionRead])
async def listar_descripciones_objetivo(
    objetivo_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = DescripcionService(db)
    return await service.list_by_objetivo(objetivo_id)
