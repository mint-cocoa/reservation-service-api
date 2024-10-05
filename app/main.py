from fastapi import FastAPI
from app.routers import reservations, queues, users
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.utils.redis_client import redis_client
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
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 데이터베이스 테이블 생성
from app.models import queue, facility, ride  # 새로 생성한 모델을 임포트

Base.metadata.create_all(bind=engine)

# 서비스 시작 시 줄서기용 Redis DB 생성
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        # 열린 놀이기구 조회
        open_rides = db.query(Ride).filter(Ride.is_open == True).all()
        for ride in open_rides:
            queue_key = f"queue:{ride.id}"
            # Redis에서 이미 존재하는 큐가 없으면 빈 리스트로 초기화
            if not redis_client.exists(queue_key):
                redis_client.ltrim(queue_key, 1, 0)  # 빈 리스트로 초기화
                print(f"Initialized empty queue for ride ID {ride.id}")
            else:
                print(f"Queue for ride ID {ride.id} already exists")
        # 추가 초기화 작업이 필요하면 여기에 작성
        init_redis_with_open_rides()
    except Exception as e:
        print(f"Error initializing Redis: {e}")
    finally:
        db.close()
        print("Redis DB initialized.")