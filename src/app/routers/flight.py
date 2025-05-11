from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.flight import FlightAddRequest, FlightSearchRequest, FlightSearchResponse
from app.config.database import get_db
from app.service.flight import add_flight_service, search_flight_service, search_flight_all_service
from app.service.security import get_current_admin

router = APIRouter(prefix="/flight", tags=["Flight"])

@router.post("/search_flight/", response_model=List[FlightSearchResponse])
def search_flight(request: FlightSearchRequest, db: Session = Depends(get_db)):
    return search_flight_service(request, db)

@router.post("/add_flight/")
def add_flight(request: FlightAddRequest, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    return add_flight_service(request, db)

@router.get("/search_flight_all/")
def search_flight_all(db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    return search_flight_all_service(db)