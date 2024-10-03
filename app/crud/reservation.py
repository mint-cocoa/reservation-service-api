import uuid
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.utils.redis_client import redis_client
from typing import List

RESERVATION_KEY = "reservations"

def create_reservation(reservation: ReservationCreate) -> str:
    reservation_id = str(uuid.uuid4())
    reservation_data = reservation.dict()
    redis_client.hset(RESERVATION_KEY, reservation_id, str(reservation_data))
    return reservation_id

def get_reservations() -> List[ReservationResponse]:
    reservations = redis_client.hgetall(RESERVATION_KEY)
    reservation_list = []
    for res_id, res_data in reservations.items():
        # Assuming res_data is stored as string representation of dict
        res_dict = eval(res_data)
        reservation = ReservationResponse(id=res_id, **res_dict)
        reservation_list.append(reservation)
    return reservation_list
