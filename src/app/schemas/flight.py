from datetime import date, datetime
from typing import List
from pydantic import BaseModel

class FlightSearchRequest(BaseModel):
    departure_airport_code: str # Mã sân bay khởi hành
    arrival_airport_code: str # Mã sân bay đến nơi
    departure_time: date # Ngày khởi hành
    ticket_classes: str | None = None # Hạng vé (economy, business,...)
    number_adults: int = 1 # Số lượng người lớn
    number_children: int = 0 # Số lượng trẻ em
    number_infants: int = 0 # Số lượng em bé
    
class FlightSearchResponse(BaseModel):
    airline_name: str # Tên hãng hàng không
    flight_number: str # Số hiệu chuyến bay
    departure_airport: str # Tên sân bay khởi hành
    arrival_airport: str # Tên sân bay đến nơi
    departure_time: datetime # Thời gian khởi hành
    arrival_time: datetime # Thời gian đến nơi
    ticket_class_name: str # Tên hạng vé (economy, business,...)
    available_seats: int # Số ghế còn trống
    total_price: float # Tổng giá vé cho tất cả hành khách
    
class FlightSearchAllResponse(BaseModel):
    flight_id: int # ID chuyến bay
    flight_number: str # Số hiệu chuyến bay
    airline_name: str # Tên hãng hàng không
    departure_airport_code: str # Tên sân bay khởi hành
    arrival_airport_code: str # Tên sân bay đến nơi
    departure_time: datetime # Thời gian khởi hành
    arrival_time: datetime # Thời gian đến nơi
    available_seats: int # Số ghế còn trống
    price_tables: List['PriceTable'] # Bảng giá cho các hạng vé khác nhau
    
class PriceTable(BaseModel):
    ticket_class_name: str  # Tên hạng vé (economy, business,...)
    adult_price: float  # Giá vé người lớn
    child_price: float  # Giá vé trẻ em
    infant_price: float  # Giá vé em bé
    
class FlightAddRequest(BaseModel):
    flight_number: str # Số hiệu chuyến bay
    airline_name: str # Tên hãng hàng không
    departure_airport_code: str # Mã sân bay khởi hành
    arrival_airport_code: str # Mã sân bay đến nơi
    departure_time: datetime # Ngày khởi hành
    arrival_time: datetime # Ngày đến nơi
    available_seats: int # Số ghế còn trống
    price_tables: List[PriceTable] # Bảng giá cho các hạng vé khác nhau
    
class FlightUpdateRequest(BaseModel):
    flight_id: int # ID chuyến bay
    flight_number: str # Số hiệu chuyến bay
    airline_name: str # Tên hãng hàng không
    departure_airport_code: str # Mã sân bay khởi hành
    arrival_airport_code: str # Mã sân bay đến nơi
    departure_time: datetime # Ngày khởi hành
    arrival_time: datetime # Ngày đến nơi
    available_seats: int # Số ghế còn trống
    price_tables: List[PriceTable] # Bảng giá cho các hạng vé khác nhau
    
class FlightDeleteRequest(BaseModel):
    flight_ids: List[int] # ID chuyến bay
    
class FlightDeleteResponse(BaseModel):
    message: str
    deleted_flight_ids: List[int]
    not_found_flight_ids: List[int]
    