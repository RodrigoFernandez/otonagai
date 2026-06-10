# otonagai

Otonagai (大人買い): Es un término cultural japonés espectacular. Significa "comprar como un adulto",
y se usa específicamente cuando un adulto usa su sueldo para comprar juguetes, mangas o coleccionables
que de chico no podía permitirse. Es ideal si tu aplicación se enfoca mucho en el registro de precios
y presupuesto de compra.

API REST para seguimiento de objetivos de compra, precios y presupuesto de coleccionables.

## Stack

- Python >=3.13
- uv (gestor de paquetes y versiones de Python)
- FastAPI
- SQLAlchemy 2.0 (asíncrono)
- Alembic (migraciones)
- SQLite (vía aiosqlite, migrable a PostgreSQL)

## Desarrollo local

```bash
# 1. Clonar el repo
git clone git@github.com:RodrigoFernandez/otonagai.git
cd otonagai

# 2. Instalar y fijar versión de Python (si no está instalada)
uv python install 3.13
uv python pin 3.13

# 3. Crear entorno virtual e instalar dependencias
uv sync

# 4. Ejecutar migraciones
uv run alembic upgrade head

# 5. Iniciar servidor de desarrollo
uv run uvicorn app.main:app --reload

# 6. Abrir http://localhost:8000/docs (documentación interactiva)
```

## Variables de entorno

| Variable | Default | Descripción |
|---|---|---|
| `DATABASE_URL` | `sqlite+aiosqlite:///./otonagai.db` | URL de la base de datos |
| `UPLOAD_DIR` | `./uploads` | Directorio de imágenes subidas |

## Comandos útiles

```bash
uv sync                        # Instalar/actualizar dependencias
uv run alembic upgrade head    # Ejecutar migraciones
uv run alembic revision --autogenerate -m "descripcion"  # Crear nueva migración
uv run pytest                  # Ejecutar tests
uv run pytest -v               # Tests con verbose
uv run ruff check              # Lint
uv run ruff check --fix        # Lint con auto-fix
```

## Proyectos relacionados

- [bingobukku](https://github.com/RodrigoFernandez/bingobukku) — Versión original con FastHTML + SQLModel
