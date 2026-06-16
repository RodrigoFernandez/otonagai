# Modelo SQLAlchemy para la tabla "descripciones".
# Cada registro representa una descripción de precio observado
# en una feria/local, asociada a un objetivo.
from datetime import datetime

from sqlalchemy import Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Descripcion(Base):
    __tablename__ = "descripciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    feria: Mapped[str] = mapped_column(String(200))          # Nombre de la feria o evento
    local: Mapped[str] = mapped_column(String(200))          # Nombre del local o puesto
    moneda: Mapped[str] = mapped_column(String(10))          # Código de moneda (ARS, USD, etc.)
    precio: Mapped[float] = mapped_column(Float)             # Precio observado
    objetivo_id: Mapped[int] = mapped_column(
        ForeignKey("objetivos.id", ondelete="CASCADE")       # Si se elimina el objetivo, se eliminan sus descripciones
    )
    created_at: Mapped[datetime] = mapped_column(default=func.now())  # Fecha de creación automática

    # Relación muchos-a-uno: una descripción pertenece a un objetivo
    objetivo: Mapped["Objetivo"] = relationship(back_populates="descripciones")  # noqa: F821
