# Esquemas Pydantic para la entidad Usuario.
# Separan los datos de entrada (Create) de los de salida (Read)
# para evitar exponer información sensible como el password.
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UsuarioCreate(BaseModel):
    # Esquema usado al registrar un usuario.
    # password se envía en la request pero nunca se devuelve en respuestas.
    nombre: str
    mail: EmailStr            # Validación automática de formato email
    password: str             # Se hashea con bcrypt antes de almacenar


class UsuarioRead(BaseModel):
    # Esquema usado al devolver un usuario en las respuestas.
    # No incluye password_hash ni password por seguridad.
    id: int
    nombre: str
    mail: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UsuarioReadSimple(BaseModel):
    # Versión reducida de UsuarioRead, útil para listados o
    # referencias donde no se necesita la fecha de creación.
    id: int
    nombre: str
    mail: str

    model_config = {"from_attributes": True}
