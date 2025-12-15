"""
FastAPI Main Application - Migrado de Django/Wagtail para FastAPI + PostgreSQL
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.config import get_settings
from app.api.v1 import companies, articles, locations, sitemap, auth, admin
from app.core.templates import render_template

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API REST da Agência Kaizen - FastAPI com PostgreSQL (Migrado de Django/Wagtail)",
    debug=settings.debug,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos e mídia (se os diretórios existirem)
from pathlib import Path
static_path = Path(settings.static_root)
media_path = Path(settings.media_root)

if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
if media_path.exists():
    app.mount("/media", StaticFiles(directory=str(media_path)), name="media")

# Routers API
app.include_router(auth.router, prefix=settings.api_v1_prefix, tags=["auth"])
app.include_router(admin.router, prefix=settings.api_v1_prefix, tags=["admin"])
app.include_router(companies.router, prefix=settings.api_v1_prefix, tags=["companies"])
app.include_router(articles.router, prefix=settings.api_v1_prefix, tags=["articles"])
app.include_router(locations.router, prefix=settings.api_v1_prefix, tags=["locations"])
app.include_router(sitemap.router, prefix=settings.api_v1_prefix, tags=["sitemap"])

# TODO: Adicionar routers para:
# - blog (articles já existe, mas pode expandir)
# - portfolio
# - pages
# - contact
# - leads
# - cases
# - services


@app.get("/")
async def root():
    """Health check"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

