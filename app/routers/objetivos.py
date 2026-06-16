# Router con los endpoints CRUD para objetivos.
# Un objetivo es un item de seguimiento que un usuario monitorea.
# Incluye endpoints para gestión de imágenes y consulta de
# descripciones asociadas.
from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.descripcion import DescripcionRead
from app.schemas.objetivo import ObjetivoCreate, ObjetivoRead, ObjetivoUpdate
from app.services.descripcion import DescripcionService
from app.services.objetivo import ObjetivoService

router = APIRouter(prefix="/api/objetivos", tags=["objetivos"])


# @router.post: endpoint POST para crear un nuevo objetivo
# response_model: esquema que define qué campos se devuelven
# status_code=201: respuesta estándar para creación exitosa
@router.post("/", response_model=ObjetivoRead, status_code=status.HTTP_201_CREATED)
async def crear_objetivo(
    # data: el body JSON se parsea y valida contra ObjetivoCreate
    data: ObjetivoCreate,
    db: AsyncSession = Depends(get_db),
):
    # Crea un nuevo objetivo. Requiere nombre y usuario_id en el body.
    service = ObjetivoService(db)
    return await service.create(data)


# @router.get con path parameter: obtiene un recurso por ID
@router.get("/{objetivo_id}", response_model=ObjetivoRead)
async def obtener_objetivo(
    # objetivo_id: path parameter extraído de la URL
    objetivo_id: int,
    db: AsyncSession = Depends(get_db),
):
    # Obtiene un objetivo por su ID, incluyendo sus descripciones
    # asociadas. Retorna 404 si no existe.
    service = ObjetivoService(db)
    return await service.get_by_id(objetivo_id)


# response_model=list[ObjetivoRead]: indica que la respuesta es una lista
# de esquemas, FastAPI la serializa como un array JSON
@router.get("/", response_model=list[ObjetivoRead])
async def listar_objetivos(
    # usuario_id: query parameter opcional (?usuario_id=5).
    # Optional[int] = None lo hace opcional; si no se envía es None
    usuario_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    # Lista objetivos. Si se pasa usuario_id como query parameter,
    # filtra solo los objetivos de ese usuario. Si no, retorna todos.
    service = ObjetivoService(db)
    return await service.list_by_usuario(usuario_id)


# @router.put: endpoint HTTP PUT para actualizar un recurso existente
# (reemplazo parcial en este caso, similar a PATCH)
@router.put("/{objetivo_id}", response_model=ObjetivoRead)
async def actualizar_objetivo(
    objetivo_id: int,
    # data: body validado contra ObjetivoUpdate (todos los campos opcionales)
    data: ObjetivoUpdate,
    db: AsyncSession = Depends(get_db),
):
    # Actualiza parcialmente un objetivo (PATCH semantics).
    # Por ahora solo permite modificar el nombre.
    # Retorna 404 si el objetivo no existe.
    service = ObjetivoService(db)
    return await service.update(objetivo_id, data)


@router.delete("/{objetivo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_objetivo(
    objetivo_id: int,
    db: AsyncSession = Depends(get_db),
):
    # Elimina un objetivo y todas sus descripciones asociadas
    # (por el cascade definido en el modelo). Retorna 404 si no existe.
    service = ObjetivoService(db)
    await service.delete(objetivo_id)


# UploadFile: tipo especial de FastAPI para manejar subida de archivos.
# Lee el archivo del body como multipart/form-data automáticamente.
@router.post("/{objetivo_id}/imagen", response_model=ObjetivoRead)
async def subir_imagen_objetivo(
    objetivo_id: int,
    # file: archivo subido, FastAPI lo extrae del form data
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
):
    # Sube una imagen para un objetivo. El archivo se guarda en
    # upload_dir/<objetivo_id>/ con un nombre UUID y la URL se
    # almacena en el campo imagen del objetivo.
    service = ObjetivoService(db)
    return await service.upload_image(objetivo_id, file)


@router.get("/{objetivo_id}/descripciones", response_model=list[DescripcionRead])
async def listar_descripciones_objetivo(
    objetivo_id: int,
    db: AsyncSession = Depends(get_db),
):
    # Obtiene todas las descripciones asociadas a un objetivo,
    # ordenadas por ID ascendente.
    service = DescripcionService(db)
    return await service.list_by_objetivo(objetivo_id)
