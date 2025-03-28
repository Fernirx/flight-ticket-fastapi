from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from fastapi import HTTPException
from app.models.flights import Flight
from app.models.airports import Airport
from app.models.ticket_classes import TicketClass
from app.schemas.ticket_flight import FlightSearchRequest, BookingItemResponse
from datetime import datetime

def search_tickets_service(request: FlightSearchRequest, db: Session) -> List[BookingItemResponse]:
    try:
        departure_date = datetime.strptime(request.departure_date, "%Y-%m-%d")
        if request.return_date:
            return_date = datetime.strptime(request.return_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Ngày đi hoặc ngày về không hợp lệ")

    departure_airport = db.query(Airport).filter(Airport.code == request.departure_location).first()
    arrival_airport = db.query(Airport).filter(Airport.code == request.destination_location).first()

    if not departure_airport or not arrival_airport:
        raise HTTPException(status_code=404, detail="Không tìm thấy sân bay khởi hành hoặc sân bay đến")

    filters = [
        Flight.departure_airport_id == departure_airport.id,
        Flight.arrival_airport_id == arrival_airport.id,
        Flight.departure_time >= departure_date,
        Flight.departure_time < datetime(departure_date.year, departure_date.month, departure_date.day, 23, 59, 59)
    ]

    flights = db.query(Flight).filter(and_(*filters)).all()

    if not flights:
        raise HTTPException(status_code=404, detail="Không tìm thấy chuyến bay phù hợp")

    if request.ticket_class_id:
        ticket_class = db.query(TicketClass).filter(TicketClass.id == request.ticket_class_id).first()
        if not ticket_class:
            raise HTTPException(status_code=404, detail="Không tìm thấy hạng vé")

    result = []
    for flight in flights:
        price = flight.base_price
        if request.ticket_class_id:
            price *= ticket_class.price_multiplier

        result.append(BookingItemResponse(
            airline_name=flight.airline,  
            flight_number=flight.flight_number,
            departure_time=flight.departure_time.strftime("%H:%M"),
            arrival_time=flight.arrival_time.strftime("%H:%M"),
            departure_airport_code=departure_airport.code,
            arrival_airport_code=arrival_airport.code,
            time_fly="03:00",  
            price=price,
            is_direct=True 
        ))

    return result