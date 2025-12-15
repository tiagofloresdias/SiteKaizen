"""
Modelos SQLAlchemy para Blog - Migrado de Django/Wagtail
"""
from sqlalchemy import Column, String, Text, Boolean, Integer, Date, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db import Base

# Tabela de associação Many-to-Many para tags
article_tags = Table(
    'article_tags',
    Base.metadata,
    Column('article_id', UUID(as_uuid=True), ForeignKey('articles.id'), primary_key=True),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tags.id'), primary_key=True),
)

# Tabela de associação Many-to-Many para categorias (artigos podem ter múltiplas categorias)
article_categories_assoc = Table(
    'article_categories_assoc',
    Base.metadata,
    Column('article_id', UUID(as_uuid=True), ForeignKey('articles.id'), primary_key=True),
    Column('category_id', UUID(as_uuid=True), ForeignKey('article_categories.id'), primary_key=True),
)


class Tag(Base):
    """Tags para artigos do blog"""
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    articles = relationship("Article", secondary=article_tags, back_populates="tags")
    
    def __repr__(self):
        return f"<Tag {self.name}>"


class ArticleCategory(Base):
    """Categoria de artigo do blog"""
    __tablename__ = "article_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(80), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    articles = relationship("Article", secondary=article_categories_assoc, back_populates="categories")
    
    def __repr__(self):
        return f"<ArticleCategory {self.name}>"


class Article(Base):
    """Artigo/Blog Post - Migrado de BlogPage"""
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    
    # Conteúdo
    intro = Column(String(250), nullable=True)  # Migrado de intro
    body = Column(Text, nullable=False)  # Migrado de body (RichTextField)
    
    # Datas
    date = Column(Date, nullable=False, index=True)  # Data de publicação
    published_at = Column(DateTime(timezone=True), nullable=True, index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Status e destaque
    is_featured = Column(Boolean, default=False, nullable=False, index=True)
    is_published = Column(Boolean, default=True, nullable=False, index=True)
    is_live = Column(Boolean, default=True, nullable=False, index=True)  # Equivalente ao live() do Wagtail
    
    # Metadata
    reading_time = Column(Integer, default=5)  # minutos
    
    # SEO
    meta_description = Column(String(160), nullable=True)
    meta_keywords = Column(String(255), nullable=True)
    seo_title = Column(String(255), nullable=True)
    
    # Imagens
    cover_image_url = Column(String(500), nullable=True)
    social_image_url = Column(String(500), nullable=True)
    
    # Relationships
    categories = relationship("ArticleCategory", secondary=article_categories_assoc, back_populates="articles")
    tags = relationship("Tag", secondary=article_tags, back_populates="articles")
    
    def __repr__(self):
        return f"<Article {self.title}>"

