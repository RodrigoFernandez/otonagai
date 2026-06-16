# Clase base declarativa de SQLAlchemy.
# Todos los modelos del proyecto heredan de esta clase.
# SQLAlchemy la usa internamente para mantener el registro de
# modelos y generar las tablas en la base de datos.
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
