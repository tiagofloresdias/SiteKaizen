"""
Endpoint para dados do Sitemap
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.company import Company
from app.models.article import Article

router = APIRouter()


@router.get("/sitemap-data")
async def get_sitemap_data(db: Session = Depends(get_db)):
    """
    Retorna dados para gerar o sitemap dinâmico.
    Inclui slugs de empresas e artigos publicados.
    """
    # Empresas ativas
    companies = (
        db.query(Company.slug)
        .filter(Company.is_active == True)
        .all()
    )
    company_slugs = [c[0] for c in companies]
    
    # Artigos publicados
    articles = (
        db.query(Article.slug)
        .filter(Article.is_published == True)
        .all()
    )
    article_slugs = [a[0] for a in articles]
    
    return {
        "companies": company_slugs,
        "articles": article_slugs,
        "static_pages": [
            "/",
            "/nossas-empresas",
            "/blog",
            "/onde-estamos",
            "/contato",
        ],
    }



