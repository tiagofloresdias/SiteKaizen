"""
Schemas Pydantic para Empresas
"""
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID


class CompanyCategoryBase(BaseModel):
    """Schema base para categoria"""
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)
    description: Optional[str] = None
    color: str = Field(default="#D62042", max_length=7)


class CompanyCategory(CompanyCategoryBase):
    """Schema completo de categoria"""
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CompanyFeatureBase(BaseModel):
    """Schema base para feature"""
    title: str = Field(..., max_length=100)
    description: str
    icon: Optional[str] = Field(None, max_length=50)
    order: int = Field(default=0, ge=0)


class CompanyFeature(CompanyFeatureBase):
    """Schema completo de feature"""
    id: UUID
    company_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CompanyBase(BaseModel):
    """Schema base para empresa"""
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)
    tagline: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    logo_url: Optional[str] = Field(None, max_length=500)
    featured_image_url: Optional[str] = Field(None, max_length=500)
    website_url: Optional[str] = Field(None, max_length=500)
    contact_email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    is_active: bool = Field(default=True)
    order: int = Field(default=0, ge=0)
    meta_description: Optional[str] = Field(None, max_length=160)
    founded_date: Optional[date] = None


class CompanyCreate(CompanyBase):
    """Schema para criar empresa"""
    category_id: UUID


class Company(CompanyBase):
    """Schema completo de empresa"""
    id: UUID
    category_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Relacionamentos
    category: CompanyCategory
    features: List[CompanyFeature] = []
    
    class Config:
        from_attributes = True


class CompanyList(BaseModel):
    """Schema para lista de empresas"""
    data: List[Company]
    total: int
    page: Optional[int] = 1
    limit: Optional[int] = 20
    pages: Optional[int] = 1



