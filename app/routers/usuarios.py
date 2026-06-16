# Router con los endpoints CRUD para usuarios.
# Incluye registro, consulta, listado y eliminación.
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioRead
from app.services.usuario import UsuarioService

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])


# @router.post: endpoint POST para crear un recurso
# response_model: define el esquema de la respuesta (excluye password)
# status_code=201: HTTP 201 Created indica que se creó un nuevo recurso
@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
async def crear_usuario(
    # data: el body JSON se deserializa y valida contra UsuarioCreate
    data: UsuarioCreate,
    # db: sesión de BD inyectada por FastAPI via Depends.
    # Depends(get_db) resuelve la dependencia get_db, que crea y
    # cierra una sesión asíncrona por cada request.
    db: AsyncSession = Depends(get_db),
):
    # Registra un nuevo usuario. Valida que el mail no esté en uso
    # (409 si ya existe) y hashea la contraseña antes de guardarla.
    service = UsuarioService(db)
    return await service.create(data)


# @router.get: endpoint GET para obtener un recurso por ID
# response_model: el esquema que define la estructura de la respuesta
@router.get("/{usuario_id}", response_model=UsuarioRead)
async def obtener_usuario(
    # usuario_id: path parameter, se extrae de la URL y se valida como int
    usuario_id: int,
    db: AsyncSession = Depends(get_db),
):
    # Obtiene un usuario por su ID. Retorna 404 si no existe.
    service = UsuarioService(db)
    return await service.get_by_id(usuario_id)


# response_model=list[UsuarioRead]: la respuesta será una lista JSON
# de objetos UsuarioRead
@router.get("/", response_model=list[UsuarioRead])
async def listar_usuarios(
    db: AsyncSession = Depends(get_db),
):
    # Lista todos los usuarios registrados, ordenados por ID.
    service = UsuarioService(db)
    return await service.list_all()


# status_code=204: HTTP 204 No Content, respuesta típica para DELETE exitoso
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_db),
):
    # Elimina un usuario y todos sus objetivos asociados (por el
    # cascade del modelo). Retorna 404 si no existe.
    service = UsuarioService(db)
    await service.delete(usuario_id)
