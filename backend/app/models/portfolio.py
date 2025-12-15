"""
Modelos SQLAlchemy para Portfolio - Migrado de Django/Wagtail
"""
from sqlalchemy import Column, String, Text, Boolean, Date, DateTime, ForeignKey, Table, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db import Base

# Tabela de associação Many-to-Many para categorias do portfolio
portfolio_categories_assoc = Table(
    'portfolio_categories_assoc',
    Base.metadata,
    Column('portfolio_item_id', UUID(as_uuid=True), ForeignKey('portfolio_items.id'), primary_key=True),
    Column('category_id', UUID(as_uuid=True), ForeignKey('portfolio_categories.id'), primary_key=True),
)


class PortfolioCategory(Base):
    """Categoria do portfolio"""
    __tablename__ = "portfolio_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(80), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    portfolio_items = relationship("PortfolioItem", secondary=portfolio_categories_assoc, back_populates="categories")
    
    def __repr__(self):
        return f"<PortfolioCategory {self.name}>"


class PortfolioItem(Base):
    """Item individual do portfolio - Migrado de PortfolioItem"""
    __tablename__ = "portfolio_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    
    # Informações do projeto
    client = Column(String(255), nullable=False)
    project_date = Column(Date, nullable=True)
    project_url = Column(String(500), nullable=True)
    
    # Conteúdo
    description = Column(Text, nullable=False)  # RichTextField convertido para Text
    
    # Status
    is_published = Column(Boolean, default=True, nullable=False, index=True)
    is_live = Column(Boolean, default=True, nullable=False, index=True)
    
    # Imagens
    featured_image_url = Column(String(500), nullable=True)
    
    # Datas
    published_at = Column(DateTime(timezone=True), nullable=True, index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # SEO
    meta_description = Column(String(160), nullable=True)
    meta_keywords = Column(String(255), nullable=True)
    
    # Relationships
    categories = relationship("PortfolioCategory", secondary=portfolio_categories_assoc, back_populates="portfolio_items")
    gallery_images = relationship("PortfolioGalleryImage", back_populates="portfolio_item", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<PortfolioItem {self.title}>"


class PortfolioGalleryImage(Base):
    """Imagens da galeria do portfolio - Migrado de PortfolioGalleryImage"""
    __tablename__ = "portfolio_gallery_images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_item_id = Column(UUID(as_uuid=True), ForeignKey('portfolio_items.id'), nullable=False)
    
    image_url = Column(String(500), nullable=False)
    caption = Column(String(250), nullable=True)
    order = Column(Integer, default=0, nullable=False)  # Para ordenação
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    portfolio_item = relationship("PortfolioItem", back_populates="gallery_images")
    
    def __repr__(self):
        return f"<PortfolioGalleryImage {self.caption or 'Sem legenda'}>"

