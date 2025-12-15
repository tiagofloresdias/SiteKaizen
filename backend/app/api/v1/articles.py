"""
Endpoints para Artigos
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import Optional
from math import ceil

from app.db import get_db
from app.models.article import Article, ArticleCategory
from app.schemas.article import Article as ArticleSchema, ArticleList

router = APIRouter()


@router.get("/articles", response_model=ArticleList)
async def list_articles(
    category: Optional[str] = Query(None, description="Filtrar por categoria slug"),
    is_featured: Optional[bool] = Query(None, description="Filtrar por destaque"),
    is_published: Optional[bool] = Query(True, description="Filtrar por publicado"),
    page: int = Query(1, ge=1, description="Página"),
    limit: int = Query(20, ge=1, le=100, description="Itens por página"),
    db: Session = Depends(get_db),
):
    """
    Lista todos os artigos com filtros opcionais.
    """
    query = db.query(Article)
    
    # Filtros
    if category:
        category_obj = db.query(ArticleCategory).filter(ArticleCategory.slug == category).first()
        if not category_obj:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        query = query.filter(Article.category_id == category_obj.id)
    
    if is_featured is not None:
        query = query.filter(Article.is_featured == is_featured)
    
    if is_published is not None:
        query = query.filter(Article.is_published == is_published)
    
    # Total antes da paginação
    total = query.count()
    
    # Ordenação: publicados mais recentes primeiro
    articles = (
        query.order_by(desc(Article.published_at), desc(Article.created_at))
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    
    return ArticleList(
        data=[ArticleSchema.model_validate(a) for a in articles],
        total=total,
        page=page,
        limit=limit,
        pages=ceil(total / limit) if total > 0 else 0,
    )


@router.get("/articles/{slug}", response_model=ArticleSchema)
async def get_article(slug: str, db: Session = Depends(get_db)):
    """
    Retorna um artigo completo.
    """
    article = (
        db.query(Article)
        .filter(Article.slug == slug)
        .filter(Article.is_published == True)
        .first()
    )
    
    if not article:
        raise HTTPException(status_code=404, detail="Artigo não encontrado")
    
    return ArticleSchema.model_validate(article)



