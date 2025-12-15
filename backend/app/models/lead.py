"""
Modelos SQLAlchemy para Leads - Migrado de Django/Wagtail
"""
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db import Base


class UTMParameters(Base):
    """Parâmetros UTM para rastreamento - Migrado de UTMParameters"""
    __tablename__ = "utm_parameters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # UTM Parameters
    utm_source = Column(String(100), nullable=True)
    utm_medium = Column(String(100), nullable=True)
    utm_campaign = Column(String(100), nullable=True)
    utm_term = Column(String(100), nullable=True)
    utm_content = Column(String(100), nullable=True)
    
    # Tracking adicional
    referrer = Column(String(500), nullable=True)
    landing_page = Column(String(500), nullable=True)
    user_agent = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    
    # Dados de sessão
    session_id = Column(String(100), nullable=True)
    device_type = Column(String(50), nullable=True)
    browser = Column(String(50), nullable=True)
    os = Column(String(50), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    leads = relationship("Lead", back_populates="utm_parameters")
    
    def __repr__(self):
        return f"<UTMParameters {self.utm_source} - {self.utm_medium}>"


class Touchpoint(Base):
    """Touchpoint - Evento de interação do lead - Migrado de Touchpoint"""
    __tablename__ = "touchpoints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey('leads.id'), nullable=False)
    
    event_type = Column(String(50), nullable=False, index=True)  # page_view, modal_open, etc
    event_data = Column(JSONB, nullable=True)  # Dados adicionais do evento
    step_number = Column(Integer, nullable=True)
    page_url = Column(String(500), nullable=True)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    lead = relationship("Lead", back_populates="touchpoints")
    
    def __repr__(self):
        return f"<Touchpoint {self.event_type} - {self.timestamp}>"


class Lead(Base):
    """Lead - Migrado de Lead"""
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Passo 1 - Dados básicos
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    
    # Passo 2 - Informações do negócio
    monthly_revenue = Column(String(50), nullable=True)
    business_area = Column(String(100), nullable=True)
    main_challenge = Column(Text, nullable=True)
    website_social = Column(String(200), nullable=True)
    
    # Tipo de lead
    lead_type = Column(String(20), default='business', nullable=False, index=True)  # business ou franchise
    
    # Dados específicos de franqueados
    current_activity = Column(String(100), nullable=True)
    experience_years = Column(String(20), nullable=True)
    franchise_timeline = Column(String(50), nullable=True)
    franchise_type = Column(String(50), nullable=True)
    investment_range = Column(String(50), nullable=True)
    additional_info = Column(Text, nullable=True)
    
    # Status do lead
    status = Column(String(20), default='step1', nullable=False, index=True)  # step1, step2, step3, completed
    
    # Dados do agendamento
    calendly_event_id = Column(String(100), nullable=True)
    scheduled_date = Column(DateTime(timezone=True), nullable=True)
    
    # Email de confirmação
    confirmation_email_sent = Column(Boolean, default=False, nullable=False)
    
    # UTM Parameters
    utm_parameters_id = Column(UUID(as_uuid=True), ForeignKey('utm_parameters.id'), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    utm_parameters = relationship("UTMParameters", back_populates="leads")
    touchpoints = relationship("Touchpoint", back_populates="lead", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Lead {self.name} - {self.email}>"

