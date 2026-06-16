from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import descripciones, objetivos, usuarios


# Ciclo de vida de la aplicación: crea el directorio de uploads al iniciar
@asynccontextmanager
async def lifespan(app: FastAPI):
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    yield


# Instancia principal de la aplicación FastAPI
app = FastAPI(title=settings.app_title, lifespan=lifespan)

# Configuración de CORS (Cross-Origin Resource Sharing).
# CORS es un mecanismo de seguridad del navegador que controla
# qué dominios pueden acceder a los recursos del servidor.
# Con allow_origins=["*"] se permite el acceso desde cualquier origen,
# útil durante desarrollo pero debería restringirse en producción.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Registro de los routers de la API.
# Un router agrupa rutas relacionadas (ej: /usuarios, /objetivos)
# permitiendo organizar el código en módulos separados en lugar de
# definir todos los endpoints en un solo archivo.
app.include_router(usuarios.router)
app.include_router(objetivos.router)
app.include_router(descripciones.router)

# Monta el directorio de uploads como contenido estático si existe
if Path(settings.upload_dir).exists():
    app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")


# Endpoint de verificación de salud del servidor.
# Es utilizado por orquestadores (Kubernetes, Docker Swarm, etc.) y
# balanceadores de carga para confirmar que la aplicación está viva y
# respondiendo correctamente. Un status distinto a "ok" indica que el
# servicio debería reiniciarse.
@app.get("/health")
async def health_check():
    return {"status": "ok"}
