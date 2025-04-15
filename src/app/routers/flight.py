from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.flight import FlightSearchRequest, FlightSearchResponse
from app.config.database import get_db
from app.service.flight import search_flight_service

router = APIRouter(prefix="/flight", tags=["Flight"])

@router.post("/search_flight/")
def search_flight(request: FlightSearchRequest, db: Session = Depends(get_db), response_model=List[FlightSearchResponse]):
    return search_flight_service(request, db)
