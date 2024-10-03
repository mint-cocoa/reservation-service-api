from fastapi import FastAPI, HTTPException
from app.routers import reservations, queues, users
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.utils.redis_client import redis_client
#from app.crud.facility import get_open_facilities
from app.init_redis import init_redis_with_open_rides
import os

app = FastAPI(
    title="Reservation Service",
    description="API for managing ride reservations using Redis.",
    version="1.0.0"
)

app.include_router(reservations.router, prefix="/reservations", tags=["Reservations"])
app.include_router(queues.router, prefix="/queues", tags=["Queues"])
app.include_router(users.router, prefix="/users", tags=["Users"])

# 환경 변수에서 데이터베이스 URL을 가져옵니다.
#DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")

#engine = create_engine(DATABASE_URL)

#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()

# 데이터베이스 테이블 생성
from app.models import queue, facility, ride  # 새로 생성한 모델을 임포트

#Base.metadata.create_all(bind=engine)

# 서비스 시작 시 줄서기용 Redis DB 생성
@app.on_event("startup")
def startup_event():
    #db = SessionLocal()
    try:
        # Fetch facility IDs from environment variable or configuration
        FACILITY_IDS = os.getenv("FACILITY_IDS")
        if FACILITY_IDS:
            specific_facility_ids = [int(fid.strip()) for fid in FACILITY_IDS.split(",")]
        else:
            specific_facility_ids = [1, 2, 3]  # Default IDs or handle as needed

        #facilities = get_specific_facilities(db, specific_facility_ids)
        # 임의의 놀이기구 데이터를 생성하여 테스트
        test_rides = [
            {"id": 101, "facility_id": 1, "capacity": 20},
            {"id": 102, "facility_id": 2, "capacity": 15},
            {"id": 103, "facility_id": 3, "capacity": 25}
        ]

        for ride in test_rides:
            redis_client.hset(f"ride:{ride['id']}", mapping={
                "status": "open",
                "capacity": ride['capacity'],
            })
        for ride in test_rides:
            # 각 놀이기구에 대한 Redis 큐 초기화
            redis_client.lpush(f"queue:{ride['facility_id']}", "init")
            redis_client.lpop(f"queue:{ride['facility_id']}")
        init_redis_with_open_rides(facility_ids=specific_facility_ids)
    finally:
        print("Redis DB initialized.")
    