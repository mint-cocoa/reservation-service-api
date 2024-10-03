import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utils.redis_client import redis_client
from app.models.ride import Base, Ride, AmusementPark

# 데이터베이스 설정
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/mydatabase')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_redis_with_open_rides(facility_ids=None):
    db = SessionLocal()
    try:
        if facility_ids:
            rides = db.query(Ride).filter(Ride.facility_id.in_(facility_ids)).all()
        else:
            rides = db.query(Ride).all()  # Or however you fetch rides
        
        for ride in rides:
            redis_client.hset(f"ride:{ride.id}", mapping={
                "status": "open",
                "capacity": ride.capacity,
                # Add other ride attributes as needed
            })
    finally:
        db.close()



#if __name__ == "__main__":
#    init_redis_with_open_rides()
