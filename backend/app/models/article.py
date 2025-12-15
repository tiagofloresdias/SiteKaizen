"""
Modelos SQLAlchemy para Artigos/Blog
"""
from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db import Base


class ArticleCategory(Base):
    """Categoria de artigo"""
    __tablename__ = "article_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(80), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    articles = relationship("Article", back_populates="category")
    
    def __repr__(self):
        return f"<ArticleCategory {self.name}>"


class Article(Base):
    """Artigo/Blog Post"""
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    excerpt = Column(Text, nullable=True)
    content = Column(Text, nullable=False)  # HTML ou Markdown
    
    # Imagens
    cover_image_url = Column(String(500), nullable=True)
    social_image_url = Column(String(500), nullable=True)
    
    # Datas
    published_at = Column(DateTime(timezone=True), nullable=True, index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Status e destaque
    is_featured = Column(Boolean, default=False, nullable=False, index=True)
    is_published = Column(Boolean, default=True, nullable=False, index=True)
    
    # Metadata
    reading_time = Column(Integer, default=5)  # minutos
    
    # SEO
    seo_title = Column(String(255), nullable=True)
    seo_description = Column(String(160), nullable=True)
    meta_keywords = Column(String(255), nullable=True)
    
    # Categorização
    category_id = Column(UUID(as_uuid=True), ForeignKey("article_categories.id"), nullable=True)
    
    # Relationships
    category = relationship("ArticleCategory", back_populates="articles")
    
    def __repr__(self):
        return f"<Article {self.title}>"



