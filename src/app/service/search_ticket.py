from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from fastapi import HTTPException
from app.models.flights import Flight
from app.models.airports import Airport
from app.models.ticket_classes import ShoppingCart
from app.schemas.ticket_flight import FlightSearchRequest, BookingItemResponse
from datetime import datetime


def search_tickets_service(request: FlightSearchRequest, db: Session) -> List[BookingItemResponse]:
    try:
        departure_date = datetime.strptime(request.departure_date, "%Y-%m-%d")
        return_date = None
        if request.return_date:
            return_date = datetime.strptime(request.return_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Ngày đi hoặc ngày về không hợp lệ")

    departure_airport = db.query(Airport).filter(Airport.code == request.departure_location).first()
    arrival_airport = db.query(Airport).filter(Airport.code == request.destination_location).first()

    if not departure_airport or not arrival_airport:
        raise HTTPException(status_code=404, detail="Không tìm thấy sân bay khởi hành hoặc sân bay đến")

    ticket_class = None
    price_multiplier = 1
    if request.ticket_class_id:
        ticket_class = db.query(ShoppingCart).filter(ShoppingCart.id == request.ticket_class_id).first()
        if not ticket_class:
            raise HTTPException(status_code=404, detail="Không tìm thấy hạng vé")
        price_multiplier = float(ticket_class.price_multiplier)

    def compute_total_price(base_price: float) -> float:
        return float(base_price) * price_multiplier * (
            request.count_adult +
            request.count_child * 0.75 +
            request.count_infant * 0.25
        )

    result = []

    filters = [
        Flight.departure_airport_id == departure_airport.id,
        Flight.arrival_airport_id == arrival_airport.id,
        Flight.departure_time >= departure_date,
        Flight.departure_time < datetime(departure_date.year, departure_date.month, departure_date.day, 23, 59, 59)
    ]

    outbound_flights = db.query(Flight).filter(and_(*filters)).all()

    if not outbound_flights:
        raise HTTPException(status_code=404, detail="Không tìm thấy chuyến bay chiều đi phù hợp")

    for flight in outbound_flights:
        total_price = compute_total_price(flight.base_price)
        departure_airport_obj = db.query(Airport).filter(Airport.id == flight.departure_airport_id).first()
        
        result.append(BookingItemResponse(
            airline_name=departure_airport_obj.name,
            flight_number=flight.flight_number,
            departure_time=flight.departure_time.strftime("%H:%M"),
            arrival_time="",
            departure_airport_code=departure_airport.code,
            arrival_airport_code=arrival_airport.code,
            time_fly="",
            price=round(total_price, 2),
            is_direct=True
        ))

    if request.trip_type == "round trip" and return_date:
        return_flights = db.query(Flight).filter(
            Flight.departure_airport_id == arrival_airport.id,
            Flight.arrival_airport_id == departure_airport.id,
            Flight.departure_time >= return_date,
            Flight.departure_time < datetime(return_date.year, return_date.month, return_date.day, 23, 59, 59)
        ).all()

        if not return_flights:
            raise HTTPException(status_code=404, detail="Không tìm thấy chuyến bay chiều về phù hợp")

        for flight in return_flights:
            total_price = compute_total_price(flight.base_price)
            departure_airport_obj = db.query(Airport).filter(Airport.id == flight.departure_airport_id).first()

            result.append(BookingItemResponse(
                airline_name=departure_airport_obj.name,
                flight_number=flight.flight_number,
                departure_time=flight.departure_time.strftime("%H:%M"),
                arrival_time="", 
                departure_airport_code=departure_airport.code,
                arrival_airport_code=arrival_airport.code,
                time_fly="",
                price=round(total_price, 2),
                is_direct=True
            ))

    return result
