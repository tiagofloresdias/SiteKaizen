"""
Modelos SQLAlchemy para Contato - Migrado de Django/Wagtail
"""
from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db import Base


class Newsletter(Base):
    """Newsletter - Migrado de Newsletter"""
    __tablename__ = "newsletters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=True)
    source = Column(String(100), default='blog_sidebar')
    page_url = Column(String(500), nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 suporta até 45 caracteres
    user_agent = Column(Text, nullable=True)
    
    # UTM Parameters
    utm_source = Column(String(100), nullable=True)
    utm_medium = Column(String(100), nullable=True)
    utm_campaign = Column(String(100), nullable=True)
    utm_term = Column(String(100), nullable=True)
    utm_content = Column(String(100), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    subscribed_at = Column(DateTime(timezone=True), server_default=func.now())
    unsubscribed_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Newsletter {self.email}>"


class ContactMessage(Base):
    """Mensagem de contato - Migrado de ContactMessage"""
    __tablename__ = "contact_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    company = Column(String(255), nullable=True)
    message = Column(Text, nullable=False)
    
    # Tracking
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    page_url = Column(String(500), nullable=True)
    
    # UTM Parameters
    utm_source = Column(String(100), nullable=True)
    utm_medium = Column(String(100), nullable=True)
    utm_campaign = Column(String(100), nullable=True)
    utm_term = Column(String(100), nullable=True)
    utm_content = Column(String(100), nullable=True)
    
    # Status
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<ContactMessage {self.name} - {self.email}>"

