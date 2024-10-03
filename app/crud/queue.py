import os
import redis
from sqlalchemy.orm import Session
from app.schemas.queue import QueueCreate

# Redis 연결 설정
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

def add_to_queue(db: Session, ride_id: str, user_id: str):
    redis_client.lpush(f"queue:{ride_id}", user_id)

def remove_from_queue(db: Session, ride_id: str) -> str:
    return redis_client.rpop(f"queue:{ride_id}")

def get_queue(db: Session, ride_id: str) -> list:
    return redis_client.lrange(f"queue:{ride_id}", 0, -1)
