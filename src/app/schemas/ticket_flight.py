from pydantic import BaseModel
from typing import Optional

class FlightSearchRequest(BaseModel):
    trip_type: str
    departure_location: str
    destination_location: str
    departure_date: str
    return_date: Optional[str] = None 
    ticket_class_id: Optional[int] = None
    count_adult: Optional[int] = 1         
    count_child: Optional[int] = 0        
    count_infant: Optional[int] = 0        

class BookingItemResponse(BaseModel):
    airline_name: str  
    flight_number: str  
    departure_time: str  
    arrival_time: str  
    departure_airport_code: str 
    arrival_airport_code: str  
    time_fly: str
    price: float  
    is_direct: bool
