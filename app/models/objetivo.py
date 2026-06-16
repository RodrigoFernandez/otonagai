# Modelo SQLAlchemy para la tabla "objetivos".
# Representa un objetivo de seguimiento de precios creado por un usuario.
# Puede tener múltiples descripciones asociadas y una imagen opcional.
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Objetivo(Base):
    __tablename__ = "objetivos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(200))          # Nombre del objetivo (ej: "Monitor 27 pulgadas")
    imagen: Mapped[Optional[str]] = mapped_column(String(500), default=None)  # URL relativa de la imagen subida
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id", ondelete="CASCADE")         # Si se elimina el usuario, se eliminan sus objetivos
    )
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    # Relación muchos-a-uno: un objetivo pertenece a un usuario
    usuario: Mapped["Usuario"] = relationship(back_populates="objetivos")  # noqa: F821
    # Relación uno-a-muchos: un objetivo puede tener varias descripciones.
    # cascade="all, delete-orphan" elimina las descripciones al borrar el objetivo.
    descripciones: Mapped[list["Descripcion"]] = relationship(
        back_populates="objetivo", cascade="all, delete-orphan"
    )  # noqa: F821
