"""
Configurações do backend FastAPI
"""
import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # App
    app_name: str = "Agência Kaizen API"
    app_version: str = "2.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database PostgreSQL
    db_name: str = os.getenv("DB_NAME", "agenciakaizen_cms")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "postgres")
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: str = os.getenv("DB_PORT", "5432")
    
    @property
    def database_url(self) -> str:
        """Retorna URL de conexão do PostgreSQL"""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    # API
    api_v1_prefix: str = "/api/v1"
    cors_origins: str = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,https://site2025.agenciakaizen.com.br,https://www.agenciakaizen.com.br"
    )
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Retorna lista de origens CORS"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # Site
    site_url: str = os.getenv("SITE_URL", "https://site2025.agenciakaizen.com.br")
    site_name: str = "Agência Kaizen"
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "django-insecure-change-me-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Media & Static
    media_root: str = os.getenv("MEDIA_ROOT", "/var/www/agenciakaizen/src/media")
    static_root: str = os.getenv("STATIC_ROOT", "/var/www/agenciakaizen/src/static")
    
    # Templates
    templates_dir: str = os.getenv("TEMPLATES_DIR", "/var/www/agenciakaizen/src/templates")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Retorna instância singleton das configurações"""
    return Settings()

