from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.queue import QueueCreate, QueueResponse
from app.crud.queue import add_to_queue, remove_from_queue, get_queue
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=QueueResponse)
def enqueue(queue: QueueCreate, db=Depends(get_db)):
    try:
        add_to_queue(db, queue.ride_id, queue.user_id)
        return {"message": f"사용자 {queue.user_id}가 {queue.ride_id} 놀이기구의 줄에 추가되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{ride_id}", response_model=QueueResponse)
def dequeue(ride_id: str, db=Depends(get_db)):
    try:
        user_id = remove_from_queue(db, ride_id)
        if user_id:
            return {"message": f"사용자 {user_id}가 {ride_id} 놀이기구의 줄에서 제거되었습니다."}
        else:
            return {"message": f"{ride_id} 놀이기구의 줄에 대기 중인 사용자가 없습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{ride_id}", response_model=List[str])
def view_queue(ride_id: str, db=Depends(get_db)):
    try:
        queue = get_queue(db, ride_id)
        return queue
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
