from datetime import timedelta
from sqlalchemy import func
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.flights import Flight
from app.models.flight_prices import FlightPrice
from app.models.ticket_classes import TicketClasses
from app.models.airports import Airport
from app.schemas.flight import FlightSearchRequest, FlightSearchResponse, FlightSearchAllResponse, PriceTable

def get_airport_by_code(db: Session, code: str) -> Airport:
    airport = db.query(Airport).filter(Airport.code == code).first()
    if not airport:
        raise HTTPException(status_code=404, detail="Sân bay không tồn tại")
    return airport

def get_airport_by_id(db: Session, id: str) -> Airport:
    airport = db.query(Airport).filter(Airport.id == id).first()
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
    departure_airport = get_airport_by_code(db, request.departure_airport_code)
    arrival_airport = None
    departure_time = request.departure_time
    departure_time_of_7_days = departure_time + timedelta(days=7)
    total_number_of_passengers = request.number_adults + request.number_children + request.number_infants
    ticket_classes = get_ticket_class_by_name(db, request.ticket_classes)
    
    if request.arrival_airport_code:  # Nếu có mã sân bay đến, thì tìm kiếm theo mã đó
        arrival_airport = get_airport_by_code(db, request.arrival_airport_code)
    
    query = db.query(Flight).filter(
        Flight.departure_airport_id == departure_airport.id,
        func.date(Flight.departure_time).between(departure_time, departure_time_of_7_days),
        Flight.available_seats >= total_number_of_passengers
    )
    
    # Nếu có mã sân bay đến, thì thêm điều kiện tìm kiếm theo mã đó
    if arrival_airport is not None:
        query = query.filter(Flight.arrival_airport_id == arrival_airport.id)
    
    flights = query.all()
    
    if not flights: 
        raise HTTPException(status_code=404, detail="Không tìm thấy chuyến bay")

    flight_prices = db.query(FlightPrice).filter(
        FlightPrice.flight_id.in_([flight.id for flight in flights]),
        FlightPrice.ticket_class_id == ticket_classes.id
    ).all()
    
    if not flight_prices:
        raise HTTPException(status_code=404, detail="Không tìm thấy giá vé")
    
    response = []
    arrival_airport_ids = [flight.arrival_airport_id for flight in flights]
    arrival_airports = db.query(Airport).filter(Airport.id.in_(arrival_airport_ids)).all()
    arrival_airport_map = {airport.id: airport for airport in arrival_airports}
    for flight in flights:
        flight_price = next((fp for fp in flight_prices if fp.flight_id == flight.id), None)
        arrival_airport = arrival_airport_map.get(flight.arrival_airport_id)
        
        if not arrival_airport:
            raise HTTPException(status_code=404, detail="Sân bay đến không tồn tại")
        
        if flight_price:
            total_price = (flight_price.adult_price * request.number_adults +
                           flight_price.child_price * request.number_children +
                           flight_price.infant_price * request.number_infants)
            
            response.append(FlightSearchResponse(
                airline_name=flight.airline_name,
                flight_number=flight.flight_number,
                departure_airport=departure_airport.code,
                arrival_airport= arrival_airport.code,
                departure_time=flight.departure_time,
                arrival_time=flight.arrival_time,
                ticket_class_name=ticket_classes.class_name,
                available_seats=flight.available_seats,
                total_price=total_price
            ))

    return response
    
def add_flight_service(request, db: Session):
    if len(request.price_tables) > 3:
        raise HTTPException(status_code=400, detail="Chỉ cho phép thêm tối đa 3 hạng vé.")
    
    if request.departure_time >= request.arrival_time:
        raise HTTPException(status_code=400, detail="Thời gian khởi hành phải trước thời gian đến")
    
    departure_airport = get_airport_by_code(db, request.departure_airport_code)
    arrival_airport = get_airport_by_code(db, request.arrival_airport_code)
    
    # Kiểm tra xem chuyến bay đã tồn tại chưa
    existing_flight = db.query(Flight).filter(
        Flight.flight_number == request.flight_number,
        Flight.departure_airport_id == departure_airport.id,
        Flight.arrival_airport_id == arrival_airport.id,
        Flight.departure_time <= request.arrival_time,
        Flight.arrival_time >= request.departure_time   
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

    for price_table in request.price_tables:
        db.add(FlightPrice(
            flight_id=new_flight.id,
            ticket_class_id=get_ticket_class_by_name(db, price_table.ticket_class_name).id,
            adult_price=price_table.adult_price,
            child_price=price_table.child_price,
            infant_price=price_table.infant_price
        ))
    db.commit()
    
    return {"message": "Thêm chuyến bay thành công", "flight_id": new_flight.id}


def search_flight_all_service(db: Session) -> List[FlightSearchResponse]:
    # Lấy danh sách các chuyến bay từ cơ sở dữ liệu
    flights = db.query(Flight).all()
    
    if not flights: 
        raise HTTPException(status_code=404, detail="Không tìm thấy chuyến bay")
    
    response = []
    for flight in flights:
        
        departure_airport = get_airport_by_id(db, flight.departure_airport_id)
        if not departure_airport:
            raise HTTPException(status_code=404, detail="Sân bay đi không tồn tại")
        
        arrival_airport = get_airport_by_id(db, flight.arrival_airport_id)
        if not arrival_airport:
            raise HTTPException(status_code=404, detail="Sân bay đến không tồn tại")
        
        response.append(FlightSearchAllResponse(
            flight_number=flight.flight_number,
            airline_name=flight.airline_name,
            departure_airport=departure_airport.code,
            arrival_airport=arrival_airport.code,
            departure_time=flight.departure_time,
            arrival_time=flight.arrival_time,
            available_seats=flight.available_seats,
            price_tables=[
                PriceTable(
                    ticket_class_name=ticket_class.class_name,
                    adult_price=flight_price.adult_price,
                    child_price=flight_price.child_price,
                    infant_price=flight_price.infant_price
                )
                for flight_price in db.query(FlightPrice).filter(FlightPrice.flight_id == flight.id).all()
                for ticket_class in db.query(TicketClasses).filter(TicketClasses.id == flight_price.ticket_class_id).all()
            ]
        ))
    return response