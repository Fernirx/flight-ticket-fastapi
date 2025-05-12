from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.flight import FlightAddRequest, FlightSearchRequest, FlightSearchResponse, FlightUpdateRequest, FlightDeleteRequest
from app.config.database import get_db
from app.service.flight import add_flight_service, update_flight_service,search_flight_service, search_flight_all_service, delete_flight_service
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

@router.put("/update_flight/")
def update_flight(request: FlightUpdateRequest, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    return update_flight_service(request, db)

@router.delete("/delete_flight/")
def delete_flight(request: FlightDeleteRequest, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    return delete_flight_service(request, db)