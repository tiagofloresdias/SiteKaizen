"""
Schemas Pydantic para Localizações
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from decimal import Decimal


class LocationBase(BaseModel):
    """Schema base para localização"""
    name: str = Field(default="Agência Kaizen", max_length=120)
    city: str = Field(..., max_length=100)
    state: str = Field(default="SP", max_length=2)
    address: str
    postal_code: Optional[str] = Field(None, max_length=12)
    country: str = Field(default="BR", max_length=2)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    maps_url: Optional[str] = Field(None, max_length=500)
    place_id: Optional[str] = Field(None, max_length=120)
    opening_hours: Optional[str] = Field(None, max_length=200)
    is_main_office: bool = Field(default=False)
    is_active: bool = Field(default=True)
    order: int = Field(default=0, ge=0)


class Location(LocationBase):
    """Schema completo de localização"""
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class LocationList(BaseModel):
    """Schema para lista de localizações"""
    data: List[Location]
    total: int



