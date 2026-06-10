# Otonagai — Contexto del proyecto

## Descripción

Otonagai (大人買い, "comprar como adulto") es una API REST para registrar y
presupuestar compras de coleccionables, mangas y juguetes. Un adulto que usa su
sueldo para comprar lo que no podía de chico.

Funcionalidad principal:
- CRUD de usuarios
- CRUD de objetivos (ítems que se quiere comprar)
- CRUD de descripciones (precios, ferias, locales donde se vio el objetivo)
- Subida de imágenes para cada objetivo

## Stack

| Componente | Tecnología |
|---|---|
| Lenguaje | Python >=3.13 |
| Package manager | uv |
| Web framework | FastAPI |
| ORM | SQLAlchemy 2.0 (asíncrono) |
| Migraciones | Alembic |
| Schemas | Pydantic v2 |
| Configuración | pydantic-settings |
| Base de datos | SQLite (via aiosqlite) — migrable a PostgreSQL |

## Arquitectura

```
app/
├── config.py        # Settings via pydantic-settings (DATABASE_URL, UPLOAD_DIR, etc.)
├── database.py      # async engine + session factory + get_db dependency
├── main.py          # FastAPI app, lifespan, routers, CORS, static files
├── models/          # SQLAlchemy ORM models (DeclarativeBase)
│   ├── base.py
│   ├── usuario.py
│   ├── objetivo.py
│   └── descripcion.py
├── schemas/         # Pydantic v2 schemas (request/response)
│   ├── usuario.py
│   ├── objetivo.py
│   └── descripcion.py
├── services/        # Business logic layer
│   ├── usuario.py
│   ├── objetivo.py
│   └── descripcion.py
└── routers/         # FastAPI routers (endpoints)
    ├── usuarios.py
    ├── objetivos.py
    └── descripciones.py
```

Flujo de datos:
```
HTTP → Router → Service (business logic) → SQLAlchemy Model → DB
                          ↕
                     Pydantic Schema (validation)
```

## Modelo de datos

```
Usuario
├── id: int (PK)
├── nombre: str
├── mail: str (unique)
├── password_hash: str
├── created_at: datetime
└── objetivos: List[Objetivo]

Objetivo
├── id: int (PK)
├── nombre: str
├── imagen: str | None
├── usuario_id: int (FK → usuario.id)
├── created_at: datetime
├── usuario: Usuario
└── descripciones: List[Descripcion]

Descripcion
├── id: int (PK)
├── feria: str
├── local: str
├── moneda: str  # "PESOS" | "DOLARES"
├── precio: float
├── objetivo_id: int (FK → objetivo.id)
├── created_at: datetime
└── objetivo: Objetivo
```

## API endpoints

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/usuarios` | Crear usuario |
| GET | `/api/usuarios/{id}` | Obtener usuario |
| GET | `/api/usuarios` | Listar usuarios |
| DELETE | `/api/usuarios/{id}` | Eliminar usuario |
| POST | `/api/objetivos` | Crear objetivo |
| GET | `/api/objetivos/{id}` | Obtener objetivo con descripciones |
| GET | `/api/objetivos` | Listar objetivos (filtro por usuario_id) |
| PUT | `/api/objetivos/{id}` | Actualizar objetivo |
| DELETE | `/api/objetivos/{id}` | Eliminar objetivo |
| POST | `/api/objetivos/{id}/imagen` | Subir imagen para objetivo |
| POST | `/api/descripciones` | Crear descripción |
| GET | `/api/descripciones/{id}` | Obtener descripción |
| GET | `/api/objetivos/{id}/descripciones` | Listar descripciones de un objetivo |
| DELETE | `/api/descripciones/{id}` | Eliminar descripción |

## Convenciones

- **Nombres**: clases en PascalCase, funciones/variables en snake_case, archivos en snake_case
- **Type hints**: obligatorios en todas las funciones
- **Imports**: estándar → terceros → locales (separados por línea en blanco)
- **Async**: todos los endpoints y servicios son async
- **Errores**: HTTPException con mensajes descriptivos
- **Servicios**: instanciar en el router con `Service(db)`, no usar singletons

## Comandos útiles

```bash
uv sync                          # Instalar dependencias
uv run uvicorn app.main:app --reload  # Servidor de desarrollo
uv run alembic upgrade head      # Ejecutar migraciones
uv run alembic revision --autogenerate -m "mensaje"  # Crear migración
uv run pytest                    # Tests
uv run ruff check                # Lint
```

## Enlaces

- Repositorio: https://github.com/RodrigoFernandez/otonagai
- Proyecto similar: https://github.com/RodrigoFernandez/bingobukku
