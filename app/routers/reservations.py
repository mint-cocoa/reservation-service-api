from fastapi import APIRouter, HTTPException
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.crud.reservation import create_reservation, get_reservations
from typing import List

router = APIRouter()

@router.post("/", response_model=ReservationResponse)
def create_new_reservation(reservation: ReservationCreate):
    reservation_id = create_reservation(reservation)
    if not reservation_id:
        raise HTTPException(status_code=400, detail="Failed to create reservation.")
    return ReservationResponse(id=reservation_id, **reservation.dict())

@router.get("/", response_model=List[ReservationResponse])
def list_reservations():
    reservations = get_reservations()
    return reservations
