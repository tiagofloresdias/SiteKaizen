"""
Modelos SQLAlchemy para Cases - Migrado de Django/Wagtail
"""
from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db import Base


class Case(Base):
    """Case de sucesso - Migrado de Case"""
    __tablename__ = "cases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    
    # Informações básicas
    client_name = Column(String(100), nullable=False)
    client_logo_url = Column(String(500), nullable=True)
    
    # Categorização
    category = Column(String(50), nullable=False, index=True)  # ecommerce, saas, servicos, etc
    
    # Conteúdo principal
    hero_image_url = Column(String(500), nullable=True)
    short_description = Column(String(300), nullable=False)
    challenge = Column(Text, nullable=False)  # RichTextField convertido
    solution = Column(Text, nullable=False)  # RichTextField convertido
    results = Column(Text, nullable=False)  # RichTextField convertido
    
    # Métricas em destaque
    main_metric_value = Column(String(50), nullable=True)
    main_metric_description = Column(String(200), nullable=True)
    
    # Conteúdo avançado (StreamField convertido para JSONB)
    content = Column(JSONB, nullable=True)
    
    # SEO
    meta_description = Column(String(160), nullable=True)
    
    # Status e datas
    is_featured = Column(Boolean, default=False, nullable=False, index=True)
    is_published = Column(Boolean, default=True, nullable=False, index=True)
    order = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Case {self.title} - {self.client_name}>"

