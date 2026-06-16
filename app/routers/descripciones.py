# Router con los endpoints CRUD para descripciones.
# Una descripción es un registro de precio observado en una
# feria/local, asociado a un objetivo.
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.descripcion import DescripcionCreate, DescripcionRead
from app.services.descripcion import DescripcionService

router = APIRouter(prefix="/api/descripciones", tags=["descripciones"])


# @router.post: define un endpoint HTTP POST en /api/descripciones/
# response_model: esquema Pydantic que valida y da forma a la respuesta
# status_code=201: indica que la creación fue exitosa (HTTP 201 Created)
@router.post("/", response_model=DescripcionRead, status_code=status.HTTP_201_CREATED)
async def crear_descripcion(
    # data: el body de la request se valida contra DescripcionCreate automáticamente
    data: DescripcionCreate,
    # db: sesión de base de datos inyectada por FastAPI mediante Depends.
    # Depends(get_db) ejecuta get_db como dependencia, creando una sesión
    # por request y cerrándola al finalizar.
    db: AsyncSession = Depends(get_db),
):
    # Crea una nueva descripción. Recibe los datos en el body
    # (DescripcionCreate) y retorna el registro creado con su ID.
    service = DescripcionService(db)
    return await service.create(data)


# @router.get con path parameter {descripcion_id}:
# el valor se extrae de la URL y se inyecta como argumento de la función
@router.get("/{descripcion_id}", response_model=DescripcionRead)
async def obtener_descripcion(
    # descripcion_id: path parameter de tipo int, validado automáticamente
    descripcion_id: int,
    db: AsyncSession = Depends(get_db),
):
    # Obtiene una descripción por su ID.
    # Retorna 404 si no existe.
    service = DescripcionService(db)
    return await service.get_by_id(descripcion_id)


@router.delete("/{descripcion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_descripcion(
    descripcion_id: int,
    db: AsyncSession = Depends(get_db),
):
    # Elimina una descripción por su ID.
    # Retorna 204 sin contenido en caso de éxito, o 404 si no existe.
    service = DescripcionService(db)
    await service.delete(descripcion_id)
