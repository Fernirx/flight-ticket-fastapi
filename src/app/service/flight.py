from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.flights import Flight
from app.models.flight_prices import FlightPrice
from app.models.ticket_classes import TicketClasses
from app.models.airports import Airport
from app.schemas.flight import FlightSearchRequest, FlightSearchResponse

def get_airport_by_code(db: Session, code: str) -> Airport:
    airport = db.query(Airport).filter(Airport.code == code).first()
    if not airport:
        raise HTTPException(status_code=404, detail="Sân bay không tồn tại")
    return airport

def get_ticket_class_by_name(db: Session, ticket_class_name: str) -> TicketClasses:
    ticket_class = db.query(TicketClasses).filter(TicketClasses.class_name == ticket_class_name).first()
    if not ticket_class:
        raise HTTPException(status_code=404, detail="Loại vé không tồn tại")
    return ticket_class

def search_flight_service(request: FlightSearchRequest, db: Session) -> List[FlightSearchResponse]:
    # Lấy danh sách các chuyến bay từ cơ sở dữ liệu
    departure_airport = get_airport_by_code(db, request.departure_location)
    arrival_airport = get_airport_by_code(db, request.arrival_location)
    flights = db.query(Flight).filter(
        Flight.departure_airport_id == departure_airport.id,
        Flight.arrival_airport_id == arrival_airport.id,
        Flight.departure_time >= request.departure_date,
        Flight.available_seats >= request.number_adults + request.number_children + request.number_infants
    ).all()
    if not flights:
        raise HTTPException(status_code=404, detail="Không tìm thấy chuyến bay nào")

    ticket_classes = get_ticket_class_by_name(db, request.ticket_classes)

    flight_prices = db.query(FlightPrice).filter(
        FlightPrice.flight_id.in_([flight.id for flight in flights]),
        FlightPrice.ticket_class_id == ticket_classes.id
    ).all()
    
    if not flight_prices:
        raise HTTPException(status_code=404, detail="Không tìm thấy giá vé cho chuyến bay này")
    
    response = []
    for flight in flights:
        flight_price = next((fp for fp in flight_prices if fp.flight_id == flight.id), None)
        if flight_price:
            total_price = (flight_price.adult_price * request.number_adults +
                           flight_price.child_price * request.number_children +
                           flight_price.infant_price * request.number_infants)
            response.append(FlightSearchResponse(
                airline_name=flight.airline_name,
                flight_number=flight.flight_number,
                departure_airport=departure_airport.code,
                arrival_airport=arrival_airport.code,
                departure_time=flight.departure_time.isoformat(),
                arrival_time=flight.arrival_time.isoformat(),
                total_price=total_price
            ))

    return response
    