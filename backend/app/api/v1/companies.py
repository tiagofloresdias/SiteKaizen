"""
Endpoints para Empresas - CRUD Completo
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from math import ceil
from uuid import UUID

from app.db import get_db
from app.models.company import Company, CompanyCategory, CompanyFeature
from app.models.user import User
from app.schemas.company import (
    Company as CompanySchema,
    CompanyList,
    CompanyCreate,
    CompanyUpdate,
    CompanyCategory as CategorySchema,
)
from app.core.auth import get_current_admin_user

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


@router.get("/companies/id/{company_id}", response_model=CompanySchema)
async def get_company_by_id(
    company_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Retorna empresa por ID (apenas admin - inclui inativas)
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    return CompanySchema.model_validate(company)


@router.post("/companies", response_model=CompanySchema, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Cria nova empresa (apenas admin)
    """
    # Verificar se slug já existe
    existing = db.query(Company).filter(Company.slug == company_data.slug).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Já existe uma empresa com este slug"
        )
    
    # Verificar se categoria existe
    category = db.query(CompanyCategory).filter(CompanyCategory.id == company_data.category_id).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )
    
    # Criar empresa
    new_company = Company(
        name=company_data.name,
        slug=company_data.slug,
        tagline=company_data.tagline,
        description=company_data.description,
        logo_url=company_data.logo_url,
        featured_image_url=company_data.featured_image_url,
        website_url=company_data.website_url,
        contact_email=company_data.contact_email,
        phone=company_data.phone,
        category_id=company_data.category_id,
        is_active=company_data.is_active,
        order=company_data.order,
        meta_description=company_data.meta_description,
        founded_date=company_data.founded_date,
    )
    
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    
    return CompanySchema.model_validate(new_company)


@router.put("/companies/{company_id}", response_model=CompanySchema)
async def update_company(
    company_id: UUID,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Atualiza empresa (apenas admin)
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    # Verificar se slug já existe (se mudou)
    if company_data.slug and company_data.slug != company.slug:
        existing = db.query(Company).filter(Company.slug == company_data.slug).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Já existe uma empresa com este slug"
            )
        company.slug = company_data.slug
    
    # Atualizar campos
    if company_data.name is not None:
        company.name = company_data.name
    if company_data.tagline is not None:
        company.tagline = company_data.tagline
    if company_data.description is not None:
        company.description = company_data.description
    if company_data.logo_url is not None:
        company.logo_url = company_data.logo_url
    if company_data.featured_image_url is not None:
        company.featured_image_url = company_data.featured_image_url
    if company_data.website_url is not None:
        company.website_url = company_data.website_url
    if company_data.contact_email is not None:
        company.contact_email = company_data.contact_email
    if company_data.phone is not None:
        company.phone = company_data.phone
    if company_data.is_active is not None:
        company.is_active = company_data.is_active
    if company_data.order is not None:
        company.order = company_data.order
    if company_data.meta_description is not None:
        company.meta_description = company_data.meta_description
    if company_data.founded_date is not None:
        company.founded_date = company_data.founded_date
    if company_data.category_id is not None:
        category = db.query(CompanyCategory).filter(CompanyCategory.id == company_data.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        company.category_id = company_data.category_id
    
    db.commit()
    db.refresh(company)
    
    return CompanySchema.model_validate(company)


@router.delete("/companies/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Deleta empresa (apenas admin)
    """
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    
    db.delete(company)
    db.commit()
    
    return None


@router.get("/company-categories", response_model=list[CategorySchema])
async def list_categories(db: Session = Depends(get_db)):
    """
    Lista todas as categorias de empresas
    """
    categories = db.query(CompanyCategory).order_by(CompanyCategory.name.asc()).all()
    return [CategorySchema.model_validate(c) for c in categories]



