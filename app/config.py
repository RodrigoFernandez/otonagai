from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # URL de conexión a la base de datos (por defecto SQLite asíncrono)
    database_url: str = "sqlite+aiosqlite:///./otonagai.db"
    # Directorio donde se almacenan los archivos subidos
    upload_dir: str = "./uploads"
    # Título de la aplicación (usado en documentación OpenAPI)
    app_title: str = "Otonagai API"
    # Orígenes permitidos para CORS (["*"] para desarrollo; restringir en producción)
    cors_origins: list[str] = ["*"]
    # Permitir envío de cookies/credenciales en peticiones cross-origin
    cors_allow_credentials: bool = True
    # Métodos HTTP permitidos (["*"] para desarrollo; restringir en producción)
    cors_allow_methods: list[str] = ["*"]
    # Headers permitidos (["*"] para desarrollo; restringir en producción)
    cors_allow_headers: list[str] = ["*"]
    allowed_image_types: list[str] = ["image/jpeg", "image/png", "image/webp"]

    # Configuración para cargar variables desde archivo .env
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


# Instancia global de configuración.
# Las variables se cargan desde un archivo .env ubicado en el directorio
# de trabajo de la aplicación. También pueden definirse como variables de
# entorno del sistema, las cuales tienen prioridad sobre el .env.
#
# Para entorno productivo, crear un archivo .env con valores específicos:
#   CORS_ORIGINS='["https://miproducto.com"]'
#   CORS_ALLOW_CREDENTIALS=true
#   CORS_ALLOW_METHODS='["GET","POST","PUT","DELETE"]'
#   CORS_ALLOW_HEADERS='["Authorization","Content-Type"]'
#   DATABASE_URL=postgresql+asyncpg://usuario:password@host:5432/db
#
# Recomendaciones:
# - No commitear el .env al repositorio; agregarlo a .gitignore.
# - En servidores, ubicarlo en el directorio de trabajo y asignarle
#   permisos restringidos (600 o 640) para evitar accesos no deseados.
# - Para múltiples entornos pueden usarse archivos como .env.development,
#   .env.production y copiar el que corresponda según el ambiente.
# - Si el .env está en otra ruta, puede especificarse con una ruta
#   absoluta en model_config, ej: "env_file": "/etc/otonagai/.env"
settings = Settings()
