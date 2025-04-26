from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.flight import FlightAddRequest, FlightSearchRequest, FlightSearchResponse
from app.config.database import get_db
from app.service.flight import add_flight_service, search_flight_service

router = APIRouter(prefix="/flight", tags=["Flight"])

@router.post("/search_flight/", response_model=List[FlightSearchResponse])
def search_flight(request: FlightSearchRequest, db: Session = Depends(get_db)):
    return search_flight_service(request, db)

@router.post("/add_flight/")
def add_flight(request: FlightAddRequest, db: Session = Depends(get_db)):
    return add_flight_service(request, db)