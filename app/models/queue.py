from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.main import Base

class Queue(Base):
    __tablename__ = "queues"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    ride_id = Column(String, nullable=False, index=True)
    user_name = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Queue(id={self.id}, ride_id={self.ride_id}, user_name={self.user_name}, is_active={self.is_active})>"
