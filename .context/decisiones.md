# Decisiones de arquitectura — Otonagai

## ADR-001: Stack tecnológico inicial

**Fecha**: 2026-06-10

### Contexto
Se necesita un backend REST para una aplicación de seguimiento de precios y
presupuesto de coleccionables. El proyecto debe ser moderno, mantenible y
permitir cambiar de base de datos en el futuro.

### Decisión

| Decisión | Elección | Alternativas consideradas |
|---|---|---|
| Package manager | uv | Poetry, pip, rye |
| Framework | FastAPI | Flask, Django, Litestar |
| ORM | SQLAlchemy 2.0 (async) | SQLModel, Django ORM, Tortoise |
| Migraciones | Alembic | — |
| Schemas | Pydantic v2 | attrs, dataclasses |
| Config | pydantic-settings | python-dotenv, environs |
| DB inicial | SQLite (aiosqlite) | — |

### Consecuencias
- SQLAlchemy 2.0 con async permite migrar a PostgreSQL sin cambiar la capa de
  acceso a datos.
- uv simplifica la gestión de versiones de Python y dependencias.
- FastAPI proporciona documentación OpenAPI automática y validación con
  Pydantic.
- El uso de async prepara el proyecto para mejor escalabilidad.

---

## ADR-002: Estructura del proyecto

**Fecha**: 2026-06-10

### Contexto
Se necesita una estructura estándar, predecible y que separe responsabilidades.

### Decisión
```
otonagai/
├── app/
│   ├── config.py        # Configuración
│   ├── database.py      # Conexión a DB
│   ├── main.py          # Punto de entrada
│   ├── models/          # ORM
│   ├── schemas/         # Validación
│   ├── services/        # Lógica de negocio
│   └── routers/         # Endpoints
├── alembic/             # Migraciones
├── tests/               # Tests
├── .context/            # Documentación de contexto
└── uploads/             # Archivos subidos
```

Capas:
- **models**: Define las tablas y relaciones (SQLAlchemy)
- **schemas**: Define la interfaz pública (Pydantic)
- **services**: Orquesta la lógica de negocio
- **routers**: Define los endpoints HTTP

### Consecuencias
- Separación clara de responsabilidades.
- Fácil de testear cada capa de forma aislada.
- Estructura familiar para cualquier desarrollador Python.

---

## ADR-003: Archivos de contexto

**Fecha**: 2026-06-10

### Contexto
Se quiere mantener una línea de desarrollo asistido por IA con opencode.

### Decisión
- `AGENTS.md` en la raíz redirige a `.context/AGENTS.md`.
- `.context/AGENTS.md` contiene el contexto completo para la IA.
- `.context/decisiones.md` almacena las ADRs (Architecture Decision Records).
- `.context/` puede crecer con más archivos según sea necesario.

### Consecuencias
- La raíz del proyecto se mantiene limpia.
- La IA tiene acceso a toda la información del proyecto desde un solo lugar.
- Queda trazabilidad de las decisiones tomadas.
