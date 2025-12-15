"""
Modelos SQLAlchemy para Empresas
"""
from sqlalchemy import Column, String, Text, Boolean, Integer, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db import Base


class CompanyCategory(Base):
    """Categoria de empresa"""
    __tablename__ = "company_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    color = Column(String(7), default="#D62042")  # Hex color
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    companies = relationship("Company", back_populates="category")
    
    def __repr__(self):
        return f"<CompanyCategory {self.name}>"


class Company(Base):
    """Empresa do Grupo Kaizen"""
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    tagline = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    
    # Logo e imagens
    logo_url = Column(String(500), nullable=True)
    featured_image_url = Column(String(500), nullable=True)
    
    # Categorização
    category_id = Column(UUID(as_uuid=True), ForeignKey("company_categories.id"), nullable=False)
    
    # URLs e contato
    website_url = Column(String(500), nullable=True)
    contact_email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Status e ordem
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    order = Column(Integer, default=0, nullable=False)
    
    # SEO
    meta_description = Column(String(160), nullable=True)
    
    # Datas
    founded_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    category = relationship("CompanyCategory", back_populates="companies")
    features = relationship("CompanyFeature", back_populates="company", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Company {self.name}>"


class CompanyFeature(Base):
    """Características/funcionalidades de uma empresa"""
    __tablename__ = "company_features"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(50), nullable=True)  # Font Awesome class
    order = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="features")
    
    def __repr__(self):
        return f"<CompanyFeature {self.title}>"



