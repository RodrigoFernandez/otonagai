from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioRead
from app.services.usuario import UsuarioService

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])


@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
async def crear_usuario(data: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    return await service.create(data)


@router.get("/{usuario_id}", response_model=UsuarioRead)
async def obtener_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    return await service.get_by_id(usuario_id)


@router.get("/", response_model=list[UsuarioRead])
async def listar_usuarios(db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    return await service.list_all()


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    await service.delete(usuario_id)
