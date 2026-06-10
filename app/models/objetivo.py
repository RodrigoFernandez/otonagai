from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Objetivo(Base):
    __tablename__ = "objetivos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(200))
    imagen: Mapped[Optional[str]] = mapped_column(String(500), default=None)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    usuario: Mapped["Usuario"] = relationship(back_populates="objetivos")  # noqa: F821
    descripciones: Mapped[list["Descripcion"]] = relationship(
        back_populates="objetivo", cascade="all, delete-orphan"
    )  # noqa: F821
