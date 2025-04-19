from datetime import date
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