from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.ticket_flight import FlightSearchRequest, BookingItemResponse
from app.service.search_ticket import search_tickets_service
from typing import List

ticket_router = APIRouter(prefix="/search", tags=["Search", "Booking"])

@ticket_router.post("/search/", response_model=List[BookingItemResponse])
def search_tickets(request: FlightSearchRequest, db: Session = Depends(get_db)):
    return search_tickets_service(request, db)