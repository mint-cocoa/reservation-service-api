import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utils.redis_client import redis_client
from app.models.ride import Base, Ride, AmusementPark

# 데이터베이스 설정
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/mydatabase')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_redis_with_open_rides():
    db = SessionLocal()
    try:
        # 열린 놀이기구 조회
        open_rides = db.query(Ride).filter(Ride.is_open == True).all()
        for ride in open_rides:
            redis_client.hset(f"ride:{ride.id}", mapping={
                "status": "open",
                "capacity": ride.max_queue_size,
                # 필요한 다른 속성 추가
            })
    except Exception as e:
        print(f"Error initializing Redis with open rides: {e}")
    finally:
        db.close()