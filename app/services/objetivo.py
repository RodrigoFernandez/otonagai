import uuid
from pathlib import Path
from typing import Optional

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.models.objetivo import Objetivo
from app.schemas.objetivo import ObjetivoCreate, ObjetivoUpdate


class ObjetivoService:
    # Servicio que encapsula la lógica de negocio relacionada con
    # objetivos: CRUD básico y carga de imágenes.

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: ObjetivoCreate) -> Objetivo:
        # Crea un nuevo objetivo y lo persiste en la base de datos.
        objetivo = Objetivo(nombre=data.nombre, usuario_id=data.usuario_id)
        self.session.add(objetivo)
        await self.session.commit()
        await self.session.refresh(objetivo)
        return objetivo

    async def get_by_id(self, objetivo_id: int) -> Objetivo:
        # Obtiene un objetivo por su ID, incluyendo sus descripciones
        # relacionadas (selectinload). Lanza 404 si no existe.
        stmt = (
            select(Objetivo)
            .where(Objetivo.id == objetivo_id)
            .options(selectinload(Objetivo.descripciones))
        )
        objetivo = await self.session.scalar(stmt)
        if not objetivo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Objetivo no encontrado"
            )
        return objetivo

    async def list_by_usuario(self, usuario_id: Optional[int] = None) -> list[Objetivo]:
        # Lista objetivos. Si se pasa usuario_id, filtra por ese usuario.
        # Si es None, retorna todos los objetivos.
        stmt = select(Objetivo)
        if usuario_id is not None:
            stmt = stmt.where(Objetivo.usuario_id == usuario_id)
        stmt = stmt.order_by(Objetivo.id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, objetivo_id: int, data: ObjetivoUpdate) -> Objetivo:
        # Actualiza los campos modificables de un objetivo.
        # Actualmente solo permite cambiar el nombre.
        objetivo = await self.session.get(Objetivo, objetivo_id)
        if not objetivo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Objetivo no encontrado"
            )
        if data.nombre is not None:
            objetivo.nombre = data.nombre
        await self.session.commit()
        await self.session.refresh(objetivo)
        return objetivo

    async def delete(self, objetivo_id: int) -> None:
        # Elimina un objetivo por su ID. Lanza 404 si no existe.
        objetivo = await self.session.get(Objetivo, objetivo_id)
        if not objetivo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Objetivo no encontrado"
            )
        await self.session.delete(objetivo)
        await self.session.commit()

    async def upload_image(self, objetivo_id: int, file: UploadFile) -> Objetivo:
        objetivo = await self.session.get(Objetivo, objetivo_id)
        if not objetivo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Objetivo no encontrado"
            )

        if file.content_type not in settings.allowed_image_types:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Tipo de archivo no permitido: {file.content_type}",
            )

        ext = Path(file.filename or "image.jpg").suffix
        filename = f"{uuid.uuid4().hex}{ext}"
        upload_path = Path(settings.upload_dir) / str(objetivo_id)
        upload_path.mkdir(parents=True, exist_ok=True)

        content = await file.read()
        (upload_path / filename).write_bytes(content)

        objetivo.imagen = f"/uploads/{objetivo_id}/{filename}"
        await self.session.commit()
        await self.session.refresh(objetivo)
        return objetivo
