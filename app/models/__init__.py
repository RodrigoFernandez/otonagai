# Exporta todos los modelos SQLAlchemy y la clase Base para que
# estén disponibles al importar app.models. Alembic y otros
# tools también usan este __init__ para descubrir los modelos.
from app.models.base import Base
from app.models.usuario import Usuario
from app.models.objetivo import Objetivo
from app.models.descripcion import Descripcion

__all__ = ["Base", "Usuario", "Objetivo", "Descripcion"]
