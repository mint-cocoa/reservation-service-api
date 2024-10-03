from pydantic import BaseModel
from datetime import datetime

class ReservationBase(BaseModel):
    ride_name: str
    user_name: str
    timestamp: datetime

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    id: str

    class Config:
        orm_mode = True
