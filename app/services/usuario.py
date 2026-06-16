import bcrypt
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate


class UsuarioService:
    # Servicio que encapsula la lógica de negocio relacionada con
    # usuarios: registro, consulta, listado y eliminación.

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: UsuarioCreate) -> Usuario:
        # Registra un nuevo usuario. Valida que el mail no esté en uso,
        # hashea la contraseña con bcrypt antes de guardarla.
        existing = await self.session.scalar(select(Usuario).where(Usuario.mail == data.mail))
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="El mail ya está registrado"
            )

        password_hash = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
        usuario = Usuario(
            nombre=data.nombre,
            mail=data.mail,
            password_hash=password_hash,
        )
        self.session.add(usuario)
        await self.session.commit()
        await self.session.refresh(usuario)
        return usuario

    async def get_by_id(self, usuario_id: int) -> Usuario:
        # Obtiene un usuario por su ID. Lanza 404 si no existe.
        usuario = await self.session.get(Usuario, usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return usuario

    async def list_all(self) -> list[Usuario]:
        # Retorna todos los usuarios registrados, ordenados por ID.
        result = await self.session.execute(select(Usuario).order_by(Usuario.id))
        return list(result.scalars().all())

    async def delete(self, usuario_id: int) -> None:
        # Elimina un usuario por su ID. Lanza 404 si no existe.
        usuario = await self.get_by_id(usuario_id)
        await self.session.delete(usuario)
        await self.session.commit()
