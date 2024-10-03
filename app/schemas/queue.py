from pydantic import BaseModel

class QueueBase(BaseModel):
    ride_id: str
    user_id: str

class QueueCreate(QueueBase):
    pass

class QueueResponse(BaseModel):
    message: str

    class Config:
        orm_mode = True
