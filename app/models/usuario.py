# Modelo SQLAlchemy para la tabla "usuarios".
# Almacena información de los usuarios registrados.
# La contraseña se guarda hasheada con bcrypt, nunca en texto plano.
from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))          # Nombre visible del usuario
    mail: Mapped[str] = mapped_column(String(255), unique=True)  # Email único por usuario
    password_hash: Mapped[str] = mapped_column(String(255))   # Hash bcrypt de la contraseña
    created_at: Mapped[datetime] = mapped_column(default=func.now())  # Fecha de registro

    # Relación uno-a-muchos: un usuario puede tener varios objetivos.
    # cascade="all, delete-orphan" asegura que al eliminar el usuario
    # se eliminen también todos sus objetivos.
    objetivos: Mapped[list["Objetivo"]] = relationship(
        back_populates="usuario", cascade="all, delete-orphan"
    )  # noqa: F821
