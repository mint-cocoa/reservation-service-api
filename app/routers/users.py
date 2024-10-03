from fastapi import APIRouter, HTTPException, Depends
from app.utils.redis_client import redis_client

router = APIRouter()

@router.post("/enqueue/{ride_id}")
def enqueue(ride_id: str, user_id: str):
    try:
        redis_client.lpush(f"queue:{ride_id}", user_id)
        return {"message": f"사용자 {user_id}가 {ride_id} 놀이기구의 줄에 추가되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dequeue/{ride_id}")
def dequeue(ride_id: str):
    try:
        user_id = redis_client.rpop(f"queue:{ride_id}")
        if user_id:
            return {"message": f"사용자 {user_id}가 {ride_id} 놀이기구의 줄에서 제거되었습니다."}
        else:
            return {"message": f"{ride_id} 놀이기구의 줄에 대기 중인 사용자가 없습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))