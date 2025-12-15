"""
Modelos SQLAlchemy para Localizações/Escritórios
"""
from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.db import Base


class Location(Base):
    """Localização/Escritório da Kaizen"""
    __tablename__ = "locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(120), nullable=False, default="Agência Kaizen")
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(2), nullable=False, default="SP")
    address = Column(Text, nullable=False)
    postal_code = Column(String(12), nullable=True)
    country = Column(String(2), nullable=False, default="BR")
    
    # Contato
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Geolocalização
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)
    
    # Google Maps
    maps_url = Column(String(500), nullable=True)
    place_id = Column(String(120), nullable=True)
    opening_hours = Column(String(200), nullable=True)  # Ex: "Mo-Fr 08:00-18:00"
    
    # Status
    is_main_office = Column(Boolean, default=False, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    order = Column(Integer, default=0, nullable=False)
    
    # Datas
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Location {self.city} - {self.address}>"



