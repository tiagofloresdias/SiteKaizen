"""
Endpoints para Localizações
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db import get_db
from app.models.location import Location
from app.schemas.location import Location as LocationSchema, LocationList

router = APIRouter()


@router.get("/locations", response_model=LocationList)
async def list_locations(
    is_active: Optional[bool] = Query(True, description="Filtrar por status ativo"),
    is_main_office: Optional[bool] = Query(None, description="Filtrar por escritório principal"),
    db: Session = Depends(get_db),
):
    """
    Lista todas as localizações com filtros opcionais.
    """
    query = db.query(Location)
    
    # Filtros
    if is_active is not None:
        query = query.filter(Location.is_active == is_active)
    
    if is_main_office is not None:
        query = query.filter(Location.is_main_office == is_main_office)
    
    # Ordenação
    locations = query.order_by(Location.order.asc(), Location.city.asc()).all()
    
    return LocationList(
        data=[LocationSchema.model_validate(l) for l in locations],
        total=len(locations),
    )



