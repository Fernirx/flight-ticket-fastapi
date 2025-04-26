from datetime import date
from typing import List
from pydantic import BaseModel

class FlightSearchRequest(BaseModel):
    departure_location: str
    arrival_location: str
    departure_date: date
    ticket_classes: str | None = None
    number_adults: int = 1
    number_children: int = 0
    number_infants: int = 0
    
class FlightSearchResponse(BaseModel):
    airline_name: str
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_time: str
    arrival_time: str
    total_price: float
    
class PriceTable(BaseModel):
    ticket_class_name: str  # Tên hạng vé (economy, business,...)
    adult_price: float  # Giá vé người lớn
    children_price: float  # Giá vé trẻ em
    infant_price: float  # Giá vé em bé
    
class FlightAddRequest(BaseModel):
    flight_number: str
    airline_name: str
    departure_airport_code: str
    arrival_airport_code: str
    departure_time: date
    arrival_time: date
    available_seats: int
    price_tables: List[PriceTable]
    
    
    