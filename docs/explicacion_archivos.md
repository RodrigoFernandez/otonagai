# Archivos de configuración del proyecto

## AGENTS.md

Archivo de contexto para asistentes de IA (como opencode). Define instrucciones globales que el asistente debe seguir al trabajar en el proyecto, como qué archivos de contexto secundarios leer o qué convenciones respetar. No afecta al código ni a herramientas de build; es puramente para orientación del agente.

## alembic.ini

Archivo de configuración de **Alembic**, la herramienta de migraciones de bases de datos para SQLAlchemy. Define la ubicación de los scripts de migración (`script_location = alembic`), la URL de conexión a la base de datos (`sqlalchemy.url`), y la configuración de logging. Es el punto de entrada que Alembic lee al ejecutar comandos como `alembic revision --autogenerate` o `alembic upgrade head`.

## script.py.mako

**Template** (en formato Mako) que usa Alembic al generar nuevas migraciones con `alembic revision`. Cuando se crea una revisión, Alembic procesa este template sustituyendo variables como `message`, `up_revision`, `create_date`, etc., para producir el archivo Python de migración listo para editar. Sirve para personalizar el esqueleto de todas las migraciones futuras.

## pyproject.toml

Archivo estándar de Python (PEP 621) que centraliza la configuración del proyecto. Define metadatos (nombre, versión, descripción), dependencias de producción y desarrollo, y settings de herramientas como `pytest` y `ruff`. Reemplaza archivos tradicionales como `setup.py`, `setup.cfg`, `requirements.txt` y `pytest.ini` en proyectos modernos.

