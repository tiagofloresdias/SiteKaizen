"""
Endpoints para Empresas
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from math import ceil

from app.db import get_db
from app.models.company import Company, CompanyCategory
from app.schemas.company import Company as CompanySchema, CompanyList

router = APIRouter()


@router.get("/companies", response_model=CompanyList)
async def list_companies(
    category: Optional[str] = Query(None, description="Filtrar por categoria slug"),
    is_active: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    page: int = Query(1, ge=1, description="Página"),
    limit: int = Query(20, ge=1, le=100, description="Itens por página"),
    db: Session = Depends(get_db),
):
    """
    Lista todas as empresas com filtros opcionais.
    """
    query = db.query(Company)
    
    # Filtros
    if category:
        category_obj = db.query(CompanyCategory).filter(CompanyCategory.slug == category).first()
        if not category_obj:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        query = query.filter(Company.category_id == category_obj.id)
    
    if is_active is not None:
        query = query.filter(Company.is_active == is_active)
    
    # Total antes da paginação
    total = query.count()
    
    # Ordenação e paginação
    companies = (
        query.order_by(Company.order.asc(), Company.name.asc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    
    return CompanyList(
        data=[CompanySchema.model_validate(c) for c in companies],
        total=total,
        page=page,
        limit=limit,
        pages=ceil(total / limit) if total > 0 else 0,
    )


@router.get("/companies/{slug}", response_model=CompanySchema)
async def get_company(slug: str, db: Session = Depends(get_db)):
    """
    Retorna detalhes de uma empresa específica.
    """
    company = (
        db.query(Company)
        .filter(Company.slug == slug)
        .filter(Company.is_active == True)
        .first()
    )
    
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    return CompanySchema.model_validate(company)



