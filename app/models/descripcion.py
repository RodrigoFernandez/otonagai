from datetime import datetime

from sqlalchemy import Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Descripcion(Base):
    __tablename__ = "descripciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    feria: Mapped[str] = mapped_column(String(200))
    local: Mapped[str] = mapped_column(String(200))
    moneda: Mapped[str] = mapped_column(String(10))
    precio: Mapped[float] = mapped_column(Float)
    objetivo_id: Mapped[int] = mapped_column(ForeignKey("objetivos.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    objetivo: Mapped["Objetivo"] = relationship(back_populates="descripciones")  # noqa: F821
