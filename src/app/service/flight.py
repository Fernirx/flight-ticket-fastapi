from datetime import timedelta
from sqlalchemy import func
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

def get_airport_by_id(db: Session, code: str) -> Airport:
    airport = db.query(Airport).filter(Airport.id == code).first()
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
    arrival_airport = None
    
    if request.arrival_location:  # Nếu có điểm đến, lấy thông tin điểm đến
        arrival_airport = get_airport_by_code(db, request.arrival_location)

    query = db.query(Flight).filter(
        Flight.departure_airport_id == departure_airport.id,
        func.date(Flight.departure_time).between(request.departure_date, request.departure_date + timedelta(days=7)),
        Flight.available_seats >= request.number_adults + request.number_children + request.number_infants
    )
    
    if arrival_airport is not None:
        query = query.filter(Flight.arrival_airport_id == arrival_airport.id)
    
    flights = query.all()
    
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
        arrival_airport = get_airport_by_id(db, flight.arrival_airport_id) if flight.arrival_airport_id else None
        
        if flight_price:
            total_price = (flight_price.adult_price * request.number_adults +
                           flight_price.child_price * request.number_children +
                           flight_price.infant_price * request.number_infants)
            response.append(FlightSearchResponse(
                airline_name=flight.airline_name,
                flight_number=flight.flight_number,
                departure_airport=departure_airport.code,
                arrival_airport= arrival_airport.code if arrival_airport else None,
                departure_time=flight.departure_time.isoformat(),
                arrival_time=flight.arrival_time.isoformat(),
                total_price=total_price
            ))

    return response
    
def add_flight_service(request, db: Session):
    if len(request.price_tables) > 3:
        raise HTTPException(status_code=400, detail="Chỉ cho phép thêm tối đa 3 hạng vé.")
    
    departure_airport = get_airport_by_code(db, request.departure_airport_code)
    arrival_airport = get_airport_by_code(db, request.arrival_airport_code)
    
    # Kiểm tra xem chuyến bay đã tồn tại chưa
    existing_flight = db.query(Flight).filter(
        Flight.flight_number == request.flight_number,
        Flight.departure_airport_id == departure_airport.id,
        Flight.arrival_airport_id == arrival_airport.id,
        func.date(Flight.departure_time) == request.departure_time
    ).first()

    if existing_flight:
        raise HTTPException(status_code=400, detail="Chuyến bay đã tồn tại")

    # Tạo đối tượng chuyến bay mới
    new_flight = Flight(
        flight_number=request.flight_number,
        airline_name=request.airline_name,
        departure_airport_id=departure_airport.id,
        arrival_airport_id=arrival_airport.id,
        departure_time=request.departure_time,
        arrival_time=request.arrival_time,
        available_seats=request.available_seats
    )
    
    db.add(new_flight)
    db.commit()
    db.refresh(new_flight)

    # Tạo đối tượng giá vé mới

    for price_table in request.price_tables:
        db.add(FlightPrice(
            flight_id=new_flight.id,
            ticket_class_id=get_ticket_class_by_name(db, price_table.ticket_class_name).id,
            adult_price=price_table.adult_price,
            child_price=price_table.children_price,
            infant_price=price_table.infant_price
        ))
    db.commit()
    
    return {"message": "Thêm chuyến bay thành công", "flight_id": new_flight.id}