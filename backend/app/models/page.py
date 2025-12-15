"""
Modelos SQLAlchemy para Páginas Padrão - Migrado de Django/Wagtail StandardPage
"""
from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db import Base


class StandardPage(Base):
    """
    Página padrão/evergreen - Migrado de StandardPage do Wagtail
    """
    __tablename__ = "standard_pages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    
    # Conteúdo
    intro = Column(Text, nullable=True)  # RichTextField convertido
    body = Column(JSONB, nullable=True)  # StreamField convertido para JSONB (mantém estrutura de blocos)
    
    # Status
    is_published = Column(Boolean, default=True, nullable=False, index=True)
    is_live = Column(Boolean, default=True, nullable=False, index=True)
    
    # Metadata
    reading_time = Column(Integer, default=5)  # minutos
    
    # SEO
    meta_description = Column(String(160), nullable=True)
    meta_keywords = Column(String(255), nullable=True)
    seo_title = Column(String(255), nullable=True)
    
    # Imagens
    social_image_url = Column(String(500), nullable=True)
    
    # Datas
    published_at = Column(DateTime(timezone=True), nullable=True, index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<StandardPage {self.title}>"

