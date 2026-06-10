from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.descripcion import Descripcion
from app.schemas.descripcion import DescripcionCreate


class DescripcionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: DescripcionCreate) -> Descripcion:
        descripcion = Descripcion(
            feria=data.feria,
            local=data.local,
            moneda=data.moneda,
            precio=data.precio,
            objetivo_id=data.objetivo_id,
        )
        self.session.add(descripcion)
        await self.session.commit()
        await self.session.refresh(descripcion)
        return descripcion

    async def get_by_id(self, descripcion_id: int) -> Descripcion:
        descripcion = await self.session.get(Descripcion, descripcion_id)
        if not descripcion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Descripción no encontrada"
            )
        return descripcion

    async def list_by_objetivo(self, objetivo_id: int) -> list[Descripcion]:
        stmt = (
            select(Descripcion)
            .where(Descripcion.objetivo_id == objetivo_id)
            .order_by(Descripcion.id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def delete(self, descripcion_id: int) -> None:
        descripcion = await self.session.get(Descripcion, descripcion_id)
        if not descripcion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Descripción no encontrada"
            )
        await self.session.delete(descripcion)
        await self.session.commit()
