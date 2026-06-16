# Teoría: Arquitectura y Buenas Prácticas

- [1. Arquitectura en Capas](#1-arquitectura-en-capas-layered-architecture)
- [2. FastAPI vs Alternativas](#2-fastapi-vs-alternativas)
- [3. ASGI vs WSGI](#3-asgi-vs-wsgi)
- [4. SQLAlchemy Async vs Síncrono vs Tortoise-ORM](#4-sqlalchemy-async-vs-síncrono-vs-tortoise-orm)
- [5. Pydantic Schemas Separados de Modelos](#5-pydantic-schemas-separados-de-modelos)
- [6. Inyección de Dependencias con Depends](#6-inyección-de-dependencias-con-depends)
- [7. Services vs Lógica en Routers o Modelos](#7-services-vs-lógica-en-routers-o-modelos-fat-models--thin-models)
- [8. Manejo de Errores](#8-manejo-de-errores)
- [9. Status Codes HTTP y Diseño RESTful](#9-status-codes-http-y-diseño-restful)
- [10. Testing](#10-testing)
- [11. Deployment](#11-deployment-despliegue)
- [12. Configuración con Pydantic Settings](#12-configuración-con-pydantic-settings)
- [13. Otras Buenas Prácticas Aplicadas](#13-otras-buenas-prácticas-aplicadas)

---

## 1. Arquitectura en Capas (Layered Architecture)

Este proyecto organiza el código en tres capas principales, donde cada una tiene una responsabilidad bien definida y se comunica únicamente con la capa adyacente:

```
┌─────────────────────────────────────────────────────────┐
│                     ROUTERS                              │
│              Capa de presentación (HTTP)                 │
│                                                          │
│  • Define rutas y métodos HTTP (GET, POST, PUT, DELETE)  │
│  • Valida datos de entrada con Pydantic schemas          │
│  • Delega la lógica a Services                           │
│  • Retorna respuestas HTTP                               │
└───────────────────────┬─────────────────────────────────┘
                        │  llama
                        ▼
┌─────────────────────────────────────────────────────────┐
│                     SERVICES                             │
│              Capa de lógica de negocio                    │
│                                                          │
│  • Contiene las reglas de negocio                        │
│  • Orquesta operaciones sobre la BD                      │
│  • Maneja errores de dominio (HTTPException)             │
│  • Independiente de FastAPI (solo usa SQLAlchemy)        │
└───────────────────────┬─────────────────────────────────┘
                        │  usa
                        ▼
┌─────────────────────────────────────────────────────────┐
│                     MODELS                               │
│              Capa de persistencia (datos)                 │
│                                                          │
│  • Modelos SQLAlchemy (mapeo objeto-relacional)          │
│  • Define tablas, columnas, relaciones y constraints     │
│  • No contiene lógica de negocio                         │
└─────────────────────────────────────────────────────────┘
```

**Flujo completo de una request:**

```
Cliente ──HTTP──▶ Router ── llama ──▶ Service ── consulta ──▶ Model ── SQL ──▶ BD
                  │                     │                      │
                  │   response_model    │  retorna modelo      │  filas
                  ◀────────────────────◀──────────────────────◀
                  │
Cliente ◀── JSON ──┘
```

### Comparativa con otras arquitecturas

| Aspecto | Capas (este proyecto) | Monolítico sin capas | Hexagonal / Clean Architecture |
|---|---|---|---|
| Separación de responsabilidades | ✅ Alta | ❌ Baja (todo mezclado) | ✅ Alta |
| Complejidad inicial | Baja | Mínima | Alta |
| Curva de aprendizaje | Baja | Ninguna | Alta |
| Testabilidad | Media (services testing) | Baja (difícil aislar) | Alta (ports/adapters) |
| Cambio de BD | Media (solo models) | Difícil (lógica dispersa) | Fácil (adapters) |
| Cambio de framework HTTP | Media (solo routers) | Difícil | Fácil |
| Ideal para | APIs REST tamaño medio | Prototipos/scripts | Sistemas grandes/complejos |

**¿Por qué capas para este proyecto?** Porque ofrece un equilibrio óptimo entre simplicidad y organización. Es fácil de entender para alguien que está aprendiendo, pero lo suficientemente estructurado como para escalar. No introduce la sobrecarga de abstracciones que trae hexagonal (puertos, adaptadores, interfaces) que pueden ser abrumadoras al empezar.

---

## 2. FastAPI vs Alternativas

FastAPI es el framework elegido para este proyecto. A continuación se compara con las alternativas más comunes en el ecosistema Python:

| Característica | FastAPI | Flask | Django |
|---|---|---|---|
| **Async nativo** | ✅ Sí, desde el inicio | ❌ No (parcial con hilos) | ✅ Sí (desde 3.0) |
| **Validación integrada** | ✅ Pydantic (automática) | ❌ Manual o Flask-Marshmallow | ✅ DRF Serializers |
| **Documentación OpenAPI** | ✅ Automática (/docs, /redoc) | ❌ Flask-Swagger (externo) | ✅ DRF-YASG (externo) |
| **Tipado** | ✅ Type hints obligatorios | ❌ Opcional | ❌ Opcional |
| **Inyección de dependencias** | ✅ Integrado (Depends) | ❌ Manual o Flask-Injector | ❌ Manual |
| **Rendimiento (requests/s)** | Alto | Medio | Medio |
| **Tamaño del framework** | Liviano | Liviano | Pesado (batteries included) |
| **Curva de aprendizaje** | Media | Baja | Alta |
| **ORM propio** | ❌ Usa SQLAlchemy | ❌ Usa SQLAlchemy | ✅ Django ORM |
| **Admin panel** | ❌ No incluido | ❌ No incluido | ✅ Django Admin |
| **Ideal para** | APIs REST, microservicios | Prototipos, apps pequeñas | Full-stack, apps grandes |

**¿Por qué FastAPI para este proyecto?**
- **Async nativo:** toda la pila es asíncrona (endpoints → services → BD), lo que permite manejar muchas conexiones concurrentes sin bloquear.
- **Validación automática:** con Pydantic no hay que escribir validación manual; los schemas definen tipo, formato, requerido/opcional.
- **Documentación gratuita:** Swagger UI y ReDoc se generan solos de las type hints y schemas.
- **Rendimiento:** comparable a Node.js o Go para APIs, muy por encima de Flask.

---

## 3. ASGI vs WSGI

**ASGI** (Asynchronous Server Gateway Interface) y **WSGI** (Web Server Gateway Interface) son protocolos que definen cómo un servidor web se comunica con una aplicación Python.

```
WSGI (Síncrono):

Cliente ──▶ Nginx ──▶ Gunicorn (WSGI) ──▶ Flask App
                    ┌─────────────────┐
                    │   Worker 1       │  ◀── atiende 1 request a la vez
                    │   Worker 2       │  ◀── atiende 1 request a la vez
                    │   Worker 3       │  ◀── atiende 1 request a la vez
                    └─────────────────┘
                Cada worker = 1 proceso / 1 request por vez

ASGI (Asíncrono):

Cliente ──▶ Nginx ──▶ Uvicorn (ASGI) ──▶ FastAPI App
                    ┌─────────────────┐
                    │   Event Loop     │  ◀── atiende N requests concurrentes
                    │   [req1][req2]   │      en un mismo proceso/hilo
                    │   [req3][req4]   │
                    └─────────────────┘
                Un solo proceso maneja múltiples requests simultáneas
```

| Característica | WSGI | ASGI |
|---|---|---|
| Modelo | Síncrono (un request por worker) | Asíncrono (event loop) |
| Concurrencia | Por procesos/hilos | Por corrutinas (cooperativa) |
| WebSockets | ❌ No soportado | ✅ Soporte nativo |
| HTTP/2 | ❌ Limitado | ✅ Soporte nativo |
| Long-polling / Server-Sent Events | ❌ Difícil | ✅ Nativo |
| Rendimiento I/O-bound | Medio | Alto (no bloquea en BD/API) |
| Complejidad | Baja | Media (concepto async/await) |

**¿Por qué ASGI?** Las operaciones de base de datos son I/O-bound (limitadas por entrada/salida): pasan la mayor parte del tiempo esperando a la BD. Con ASGI, mientras una request espera una consulta SQL, el event loop puede atender otras requests. Con WSGI, cada worker queda bloqueado esperando la respuesta de la BD, desperdiciando recursos.

---

## 4. SQLAlchemy Async vs Síncrono vs Tortoise-ORM

| Característica | SQLAlchemy Async | SQLAlchemy Síncrono | Tortoise-ORM |
|---|---|---|---|
| **Async nativo** | ✅ Sí | ❌ No (bloquea event loop) | ✅ Sí |
| **Madurez** | Alta (12+ años) | Alta (20+ años) | Media (5+ años) |
| **Ecosistema** | Amplio (Alembic, etc.) | Amplio | Limitado |
| **Curva de aprendizaje** | Alta | Alta | Media |
| **Type hints** | ✅ Mapped, mapped_column | ❌ Legacy (imperative) | ✅ Sí |
| **Relaciones** | ✅ relationship, selectinload | ✅ Ídem | ✅ FK, related_name |
| **Migraciones** | ✅ Alembic | ✅ Alembic | ✅ Aerich |
| **Rendimiento** | Alto (no bloquea) | Medio (bloquea) | Alto |
| **Sintaxis** | Verbosa | Verbosa | Concisa |

```python
# SQLAlchemy Async (este proyecto)
stmt = select(Usuario).where(Usuario.mail == data.mail)
result = await self.session.execute(stmt)
usuario = result.scalar()

# Tortoise-ORM (alternativa)
usuario = await Usuario.filter(mail=data.mail).first()
```

**SQLAlchemy `async_sessionmaker` y `expire_on_commit=False`:**

```python
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

- `async_sessionmaker`: fábrica que crea sesiones asíncronas. Similar a `sessionmaker` pero para async.
- `class_=AsyncSession`: indica que queremos sesiones asíncronas (usa `await session.get()`, `await session.execute()`, etc.).
- `expire_on_commit=False`: evita que SQLAlchemy expire (invalide) todos los objetos tras un commit. Sin esto, acceder a atributos post-commit requiere un refresh explícito.

**¿Por qué SQLAlchemy async?** Es el ORM más maduro del ecosistema Python. Tortoise-ORM es más simple pero tiene menos comunidad, menos documentación y menos integraciones. Para un proyecto educativo, SQLAlchemy es más representativo de lo que se encuentra en la industria.

---

## 5. Pydantic Schemas Separados de Modelos

Un principio clave del proyecto es mantener **esquemas Pydantic separados de los modelos SQLAlchemy**. Esto significa que los datos que entran y salen de la API se definen independientemente de cómo se almacenan en la BD.

```
Request JSON ──▶ Schema Create ──▶ Service ──▶ Model ──▶ BD
                                                      
BD ──▶ Model ──▶ Service ──▶ Schema Read ──▶ Response JSON
```

| Enfoque | Ventajas | Desventajas |
|---|---|---|
| **Schemas separados** (este proyecto) | ✅ Control total de qué se expone | ❌ Más archivos que mantener |
| | ✅ Seguridad: no expones password_hash | ❌ Puede haber duplicación de campos |
| | ✅ Validación independiente de la BD | |
| | ✅ Los modelos pueden cambiar sin afectar la API | |
| **Modelos SQLAlchemy como schemas** | ✅ Menos archivos | ❌ Riesgo de exponer datos sensibles |
| | ✅ Menos duplicación | ❌ Acopla API al schema de BD |
| | | ❌ No puedes tener validaciones distintas |
| **Dataclasses + validación manual** | ✅ Sin dependencias externas | ❌ Mucho código repetitivo |
| | ✅ Control total | ❌ Sin validación automática |
| | | ❌ Sin documentación OpenAPI automática |

**Ejemplo concreto de por qué separar:**

```python
# Modelo en BD (contiene password_hash)
class Usuario(Base):
    password_hash: Mapped[str]  # No debe exponerse

# Schema de creación (recibe password en texto plano)
class UsuarioCreate(BaseModel):
    password: str  # Se valida, se hashea, no se guarda así

# Schema de lectura (NUNCA devuelve password_hash)
class UsuarioRead(BaseModel):
    id: int
    nombre: str
    mail: str
    created_at: datetime
    # password_hash NO está aquí → no se filtra
```

Si usáramos el modelo SQLAlchemy directamente como schema de respuesta, `password_hash` se filtraría en cada respuesta JSON. Con schemas separados, controlamos **exactamente** qué campos se exponen.

---

## 6. Inyección de Dependencias con Depends

FastAPI proporciona un sistema de inyección de dependencias integrado que permite declarar qué necesita una función para funcionar, y FastAPI se encarga de proveerlo.

```python
# En database.py
async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session  # FastAPI obtiene la sesión aquí

# En el router
@router.get("/{id}")
async def obtener_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_db),  # ← inyección
):
    ...
```

**Ciclo de vida de la sesión (`Depends(get_db)`):**

```
Request entra ──▶ FastAPI llama a get_db()
                        │
                        ▼
                 async_session() → crea sesión
                        │
                        ▼
                 yield session ← se asigna a db
                        │
                        ▼
                 Router/Service usa la sesión
                        │
                        ▼
                 Request termina (éxito o error)
                        │
                        ▼
                 Se reanuda get_db() después del yield
                        │
                        ▼
                 async with session: → cierra la sesión

Request sale ←────── session cerrada
```

| Aspecto | Depends (este proyecto) | Sesión manual |
|---|---|---|
| Apertura/cierre automático | ✅ Sí (scope = request) | ❌ Hay que llamar open/close |
| Inyección en tests | ✅ Fácil (override dependencias) | ❌ Más verboso |
| Código en routers | Limpio (solo declaras) | Repetitivo (crear/cerrar) |
| Manejo de errores | ✅ Se cierra aunque haya excepción | ❌ Puede quedar abierta |
| Visibilidad de dependencias | Explícita en firma de función | Implícita |

**Ventaja clave en testing:**

```python
# En tests, puedes sobrescribir la dependencia:
async def override_get_db():
    # Usar BD de prueba en lugar de la real
    async with test_session() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db
```

---

## 7. Services vs Lógica en Routers o Modelos (Fat Models / Thin Models)

Hay tres enfoques comunes para organizar la lógica de negocio:

### Enfoque 1: Lógica en Services (este proyecto)

```
Router ── llama ──▶ Service (lógica) ──▶ Model (datos)
```

```python
# Router: delgado, solo delega
@router.post("/")
async def crear(data: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    return await service.create(data)

# Service: contiene la lógica
class UsuarioService:
    async def create(self, data):
        existing = await self.session.scalar(...)  # validación
        password_hash = bcrypt.hashpw(...)          # hasheo
        usuario = Usuario(...)                       # creación
        self.session.add(usuario)
        await self.session.commit()
        return usuario
```

### Enfoque 2: Lógica en Routers (Fat Controllers)

```
Router (lógica + HTTP) ──▶ Model (datos)
```

```python
@router.post("/")
async def crear(data: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.scalar(...)
    if existing:
        raise HTTPException(409)
    password_hash = bcrypt.hashpw(...)
    usuario = Usuario(...)
    db.add(usuario)
    await db.commit()
    return usuario
```

### Enfoque 3: Lógica en Modelos (Fat Models)

```
Router ──▶ Model (lógica + datos)
```

```python
class Usuario(Base):
    @classmethod
    async def create(cls, session, data):
        existing = await session.scalar(...)
        if existing:
            raise ...
        password_hash = bcrypt.hashpw(...)
        usuario = cls(...)
        session.add(usuario)
        await session.commit()
        return usuario
```

### Comparativa

| Aspecto | Services (thin models) | Routers (fat controllers) | Modelos (fat models) |
|---|---|---|---|
| Responsabilidad clara | ✅ Sí | ❌ Router hace de todo | ❌ Modelo hace de todo |
| Reutilizable entre routers | ✅ Sí | ❌ Lógica pegada a un endpoint | ✅ Sí (métodos de clase) |
| Testeable sin HTTP | ✅ Sí | ❌ Depende de request/response | ✅ Sí |
| Acoplamiento a FastAPI | Bajo (solo usa SQLAlchemy) | Alto (usa HTTPException, Depends) | Bajo (solo SQLAlchemy) |
| Tamaño de archivos | Equilibrado | Routers pequeños, sin lógica | Modelos muy grandes |
| Principio de responsabilidad única | ✅ Cumple | ❌ Viola | ❌ Viola |

---

## 8. Manejo de Errores

### Propagación de errores en el proyecto

```
Service: detecta error de negocio
    │
    ▼
  raise HTTPException(status_code=404, detail="...") 
    │
    ▼
FastAPI: captura la excepción automáticamente
    │
    ▼
Responde con JSON:
{
  "detail": "Usuario no encontrado"
}
Status code: 404
```

### Cómo funciona

FastAPI intercepta cualquier `HTTPException` lanzada durante el procesamiento de una request y la convierte en una respuesta JSON con el status code y mensaje correspondiente. No necesitas try/except en los routers.

```python
# En service/usuario.py
async def get_by_id(self, usuario_id: int) -> Usuario:
    usuario = await self.session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(         # ← se lanza desde el service
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario

# En el router, no hay try/except
@router.get("/{usuario_id}", response_model=UsuarioRead)
async def obtener_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    service = UsuarioService(db)
    return await service.get_by_id(usuario_id)  # HTTPException se propaga sola
```

### Errores de validación automáticos (422)

FastAPI+Pydantic generan automáticamente errores de validación:

```json
// POST /api/usuarios con body: {"nombre": "", "mail": "invalido", "password": "12"}
// Respuesta 422:
{
  "detail": [
    {
      "loc": ["body", "mail"],
      "msg": "value is not a valid email address",
      "type": "value_error"
    }
  ]
}
```

### ¿Qué pasa si no se maneja un error?

```
Error inesperado en Service
    │
    ▼
FastAPI lo captura (no HTTPException)
    │
    ▼
Responde 500 Internal Server Error
    │
    ▼
En desarrollo: muestra traceback
En producción: responde genérico (sin detalles internos)
```

### Buenas prácticas

| Error | Status Code | Cuándo usarlo |
|---|---|---|
| Recurso no existe | `404 Not Found` | `get_by_id`, `delete` |
| Conflicto (duplicado) | `409 Conflict` | mail ya registrado |
| Validación de entrada | `422 Unprocessable Entity` | Automático de Pydantic |
| Error interno | `500 Internal Server Error` | Errores no esperados |

---

## 9. Status Codes HTTP y Diseño RESTful

El proyecto utiliza códigos de estado HTTP estándar en lugar de devolver siempre 200 con un campo `status` en el body. Esto es una buena práctica RESTful.

### Códigos usados en el proyecto

| Código | Significado | Endpoints |
|---|---|---|
| `200 OK` | Éxito, respuesta con body | `GET /{id}`, `PUT /{id}`, `GET /`, `GET /{id}/descripciones` |
| `201 Created` | Recurso creado exitosamente | `POST /` |
| `204 No Content` | Éxito, sin body en respuesta | `DELETE /{id}` |
| `404 Not Found` | Recurso no existe | Cualquier `get_by_id`, `delete` |
| `409 Conflict` | Conflicto con estado actual | Crear usuario con mail existente |
| `422 Unprocessable Entity` | Datos de entrada inválidos | Automático de Pydantic |

### Por qué usar códigos HTTP estándar

```
// Enfoque RESTful (este proyecto):
HTTP 201 Created
{ "id": 1, "nombre": "Monitor", ... }

// Anti-patrón: siempre 200 con flags:
HTTP 200 OK
{ "success": true, "data": { "id": 1, "nombre": "Monitor", ... } }
```

| Aspecto | Status codes estándar | Body con flag |
|---|---|---|
| Semántica clara | ✅ El status code dice qué pasó | ❌ Hay que leer el body |
| Compatibilidad con herramientas | ✅ Caché HTTP, proxies entienden 201/204/404 | ❌ No aprovechan HTTP |
| Clientes HTTP estándar | ✅ fetch/axios manejan status codes | ❌ Solo miran el body |
| Verbosidad en respuestas vacías | ✅ 204 No Content = sin body | ❌ Siempre devuelve body |

**Ejemplo de `status_code=204` en DELETE:**

```python
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(...):
    ...
    # No hay return → FastAPI responde 204 sin body
```

Esto le indica al cliente que la operación fue exitosa pero no hay datos que devolver. El cliente sabe que no debe esperar un body JSON.

---

## 10. Testing

### Pirámide de Testing

```
          ╱╲
         ╱  ╲
        ╱ E2E╲         ← Pocos tests, lentos, caros
       ╱──────╲
      ╱Integration╲     ← Algunos tests, verifican integración
     ╱────────────╲
    ╱  Unit Tests   ╲   ← Muchos tests, rápidos, baratos
   ╱────────────────╲
```

### Unit tests (tests unitarios)

Prueban la lógica de los **services** de forma aislada, sin depender de la BD real ni de HTTP.

```python
# Estrategia: mock de la sesión SQLAlchemy
async def test_usuario_service_create_duplicate_mail():
    # mock_session devuelve un usuario existente al buscar por mail
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.scalar.return_value = Usuario(mail="test@test.com")

    service = UsuarioService(mock_session)

    with pytest.raises(HTTPException) as exc:
        await service.create(UsuarioCreate(
            nombre="Test", mail="test@test.com", password="123"
        ))

    assert exc.value.status_code == 409
```

### Integration tests (tests de integración)

Prueban los **routers** con un cliente HTTP de prueba (`TestClient`) y una BD real (por ejemplo SQLite in-memory):

```python
# Estrategia: BD de prueba + override de dependencias
@pytest.fixture
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite://", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(engine, class_=AsyncSession)

    async with async_session() as session:
        yield session

@pytest.fixture
def client(test_db):
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

### Comparativa de enfoques para la BD en tests

| Enfoque | Ventajas | Desventajas |
|---|---|---|
| **BD real (como SQLite in-memory)** | ✅ Tests realistas | ❌ Más lentos |
| | ✅ Detectan problemas de schema | ❌ Requieren setup/teardown |
| **Mock de sesión SQLAlchemy** | ✅ Muy rápidos | ❌ No detectan errores de BD |
| | ✅ Aíslan la lógica pura | ❌ Más trabajo de setup |
| **SQLite archivo temporal** | ✅ Persistente entre tests | ❌ Limpieza manual |
| | ✅ Más rápido que PostgreSQL | ❌ Diferencias con prod |

---

## 11. Deployment (Despliegue)

### 11a. Servidor Directo (bare metal / VPS)

```
                       ┌──────────────────┐
                       │    Servidor       │
                       │                  │
Cliente ──HTTPS──▶ Nginx ──proxy_pass──▶ Uvicorn ──▶ App FastAPI
                       │    :80/:443          :8000
                       │                  │
                       │    PostgreSQL ◀──┘
                       │    (o SQLite)     │
                       └──────────────────┘
```

**Pasos básicos:**

```bash
# 1. Clonar el repositorio
git clone https://github.com/user/otonagai.git && cd otonagai

# 2. Crear y activar virtualenv
python -m venv .venv && source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar DATABASE_URL, CORS_ORIGINS, etc.

# 5. Iniciar con Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Con systemd (servicio persistente):**

```ini
[Unit]
Description=Otonagai API
After=network.target

[Service]
User=otonagai
WorkingDirectory=/opt/otonagai
EnvironmentFile=/opt/otonagai/.env
ExecStart=/opt/otonagai/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### 11b. Docker

```
                    ┌─────────────────────────────────────┐
                    │        docker-compose.yml            │
                    │                                      │
                    │  ┌──────────────┐   ┌──────────────┐ │
Cliente ──HTTP──▶   │  │  nginx       │   │  app         │ │
                    │  │  :80 ──proxy──▶  │  :8000       │ │
                    │  └──────────────┘   └──────┬───────┘ │
                    │                            │         │
                    │                    ┌───────▼───────┐ │
                    │                    │  postgres     │ │
                    │                    │  :5432        │ │
                    │                    └───────────────┘ │
                    └─────────────────────────────────────┘
```

**Dockerfile:**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    volumes:
      - uploads_data:/app/uploads
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: otonagai
      POSTGRES_USER: otonagai
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pg_data:/var/lib/postgresql/data

volumes:
  uploads_data:
  pg_data:
```

### Comparativa: Servidor directo vs Docker

| Aspecto | Servidor directo | Docker |
|---|---|---|
| **Complejidad inicial** | Baja (solo Python + systemd) | Media (Dockerfile + compose) |
| **Portabilidad** | ❌ Depende del SO/config | ✅ Misma env en cualquier lado |
| **Aislamiento** | ❌ Comparte el sistema host | ✅ Contenedor aislado |
| **Escalabilidad** | Manual (más workers) | ✅ Docker Swarm / K8s |
| **Actualizaciones** | `git pull && restart` | `docker compose up -d --build` |
| **Reproducibilidad** | ❌ Depende de versión de Python/paquetes del SO | ✅ Misma imagen siempre |
| **Recursos** | Mínimo overhead | Ligero overhead del contenedor |

---

## 12. Configuración con Pydantic Settings

Pydantic Settings permite definir valores de configuración con type hints (sugerencias de tipo) y cargarlos desde múltiples fuentes: variables de entorno, archivos `.env`, o valores por defecto.

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./otonagai.db"
    upload_dir: str = "./uploads"
    cors_origins: list[str] = ["*"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

settings = Settings()
```

**Orden de prioridad (de mayor a menor):**

```
1. Variables de entorno del sistema (export DATABASE_URL=...)
                     ↑
2. Variables en archivo .env
                     ↑
3. Valores por defecto en la clase Settings
```

### ¿Por qué es mejor que usar variables sueltas o un archivo config.py manual?

| Enfoque | Ventajas | Desventajas |
|---|---|---|
| **Pydantic Settings** (este proyecto) | ✅ Validación automática de tipos | ❌ Dependencia extra |
| | ✅ Soporte `.env` nativo | |
| | ✅ Type hints | |
| | ✅ Se pueden pasar como dependencia | |
| **os.environ directamente** | ✅ Sin dependencias | ❌ Sin validación |
| | | ❌ Tipos manuales (str a int, list, etc.) |
| **config.py manual** | ✅ Sencillo | ❌ No soporta `.env` sin librería extra |
| | | ❌ Sin jerarquía de prioridades |

### Ejemplo de `.env` para producción

```env
# .env (producción)
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/otonagai
CORS_ORIGINS='["https://miproducto.com"]'
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS='["GET","POST","PUT","DELETE"]'
CORS_ALLOW_HEADERS='["Authorization","Content-Type"]'
```

### Seguridad

- No committear el `.env` al repositorio (agregar a `.gitignore`).
- En servidores, permisos `600` (solo lectura para el usuario).
- Alternativa: usar variables de entorno del sistema o un gestor de secretos (Docker secrets, HashiCorp Vault, etc.).

---

## 13. Otras Buenas Prácticas Aplicadas

### 13a. Type hints en toda la base de código

Cada función, parámetro y retorno tiene type hints:

```python
async def get_by_id(self, usuario_id: int) -> Usuario:
async def list_by_objetivo(self, objetivo_id: int) -> list[Descripcion]:
```

**Ventajas:** autocompletado en el IDE, detección temprana de errores, documentación viva, facilitan el refactoring.

### 13b. Async/await end-to-end (de principio a fin)

Toda la cadena es asíncrona, desde el router hasta la consulta a la BD:

```
async def crear() ──▶ async def service.create() ──▶ await session.execute()
```

Si mezclaras código síncrono con async, el event loop se bloquearía, anulando el beneficio de ASGI.

### 13c. Dependencia circular resuelta con import diferido + model_rebuild()

**El problema:** `ObjetivoReadWithDescripciones` necesita `DescripcionRead`, y `DescripcionRead` podría necesitar `ObjetivoRead`.

**Solución:**
```python
# objetivo.py
class ObjetivoReadWithDescripciones(ObjetivoRead):
    descripciones: list["DescripcionRead"] = []  # string forward reference

from app.schemas.descripcion import DescripcionRead  # import diferido
ObjetivoReadWithDescripciones.model_rebuild()         # resuelve la referencia
```

`model_rebuild()` es un método de Pydantic v2 que resuelve forward references después de que todas las clases están definidas.

### 13d. Cascade all, delete-orphan para integridad referencial

```python
class Usuario(Base):
    objetivos: Mapped[list["Objetivo"]] = relationship(
        back_populates="usuario", cascade="all, delete-orphan"
    )
```

- `all`: todas las operaciones en el padre se propagan a los hijos (save-update, merge, delete, etc.)
- `delete-orphan`: si un hijo se desvincula del padre, se elimina automáticamente

**Sin cascade:** al eliminar un usuario, sus objetivos quedarían huérfanos (FK apuntando a un ID que no existe) → error de integridad.

### 13e. UUID para nombres de archivo

```python
ext = os.path.splitext(file.filename or "image.jpg")[1]
filename = f"{uuid.uuid4().hex}{ext}"
```

- Evita colisiones: dos usuarios pueden subir `foto.jpg` y no se sobrescriben.
- Evita path traversal: `uuid4().hex` solo contiene caracteres hexadecimales, no puede ser `../../etc/passwd`.
- Sin información sensible: no expone nombres originales ni metadatos.

### 13f. Organización modular por entidad

```
app/
├── models/
│   ├── __init__.py
│   ├── base.py        ← Base declarativa
│   ├── usuario.py     ← Modelo Usuario
│   ├── objetivo.py    ← Modelo Objetivo
│   └── descripcion.py ← Modelo Descripcion
├── schemas/
│   ├── __init__.py
│   ├── usuario.py     ← Schemas de Usuario (Create, Read)
│   ├── objetivo.py    ← Schemas de Objetivo (Create, Read, Update)
│   └── descripcion.py ← Schemas de Descripcion (Create, Read)
├── services/
│   ├── __init__.py
│   ├── usuario.py     ← Lógica de negocio de Usuario
│   ├── objetivo.py    ← Lógica de negocio de Objetivo
│   └── descripcion.py ← Lógica de negocio de Descripcion
└── routers/
    ├── __init__.py
    ├── usuarios.py     ← Endpoints de Usuario
    ├── objetivos.py    ← Endpoints de Objetivo
    └── descripciones.py ← Endpoints de Descripcion
```

Cada entidad tiene su propio archivo en cada capa. Esto facilita encontrar código relacionado: si trabajás con usuarios, sabés que está en `models/usuario.py`, `schemas/usuario.py`, `services/usuario.py`, `routers/usuarios.py`.

### 13g. response_model para controlar datos expuestos

```python
@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
```

`response_model` le dice a FastAPI que filtre los campos del objeto retornado usando el schema indicado. Incluso si el service devolviera un objeto con más campos (como `password_hash`), FastAPI los excluiría automáticamente.

---

## Resumen

| Concepto | Decisión en el proyecto | Alternativa posible |
|---|---|---|
| Framework | FastAPI | Flask, Django |
| Protocolo | ASGI (Uvicorn) | WSGI (Gunicorn) |
| ORM | SQLAlchemy Async | Tortoise-ORM, Django ORM |
| Validación | Pydantic schemas separados | Modelos como schema |
| Arquitectura | Capas (routers/services/models) | Hexagonal, MVC |
| BD | SQLite (dev) / PostgreSQL (prod) | MySQL, MariaDB |
| Deploy | Directo o Docker | Serverless, K8s |
| Autenticación | bcrypt (planeado) | JWT, OAuth2 |
