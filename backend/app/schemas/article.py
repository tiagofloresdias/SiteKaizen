"""
Schemas Pydantic para Artigos
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import UUID


class ArticleCategoryBase(BaseModel):
    """Schema base para categoria de artigo"""
    name: str = Field(..., max_length=255)
    slug: str = Field(..., max_length=80)
    description: Optional[str] = None


class ArticleCategory(ArticleCategoryBase):
    """Schema completo de categoria"""
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ArticleBase(BaseModel):
    """Schema base para artigo"""
    title: str = Field(..., max_length=255)
    slug: str = Field(..., max_length=255)
    excerpt: Optional[str] = None
    content: str
    cover_image_url: Optional[str] = Field(None, max_length=500)
    social_image_url: Optional[str] = Field(None, max_length=500)
    is_featured: bool = Field(default=False)
    is_published: bool = Field(default=True)
    reading_time: int = Field(default=5, ge=1)
    seo_title: Optional[str] = Field(None, max_length=255)
    seo_description: Optional[str] = Field(None, max_length=160)
    meta_keywords: Optional[str] = Field(None, max_length=255)


class ArticleCreate(ArticleBase):
    """Schema para criar artigo"""
    category_id: Optional[UUID] = None
    published_at: Optional[datetime] = None


class Article(ArticleBase):
    """Schema completo de artigo"""
    id: UUID
    category_id: Optional[UUID] = None
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Relacionamentos
    category: Optional[ArticleCategory] = None
    
    class Config:
        from_attributes = True


class ArticleList(BaseModel):
    """Schema para lista de artigos"""
    data: List[Article]
    total: int
    page: Optional[int] = 1
    limit: Optional[int] = 20
    pages: Optional[int] = 1



