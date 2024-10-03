from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AmusementPark(Base):
    __tablename__ = 'amusement_parks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    rides = relationship("Ride", back_populates="amusement_park")

class Ride(Base):
    __tablename__ = 'rides'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    amusement_park_id = Column(Integer, ForeignKey('amusement_parks.id'), nullable=False)
    max_queue_size = Column(Integer, nullable=False)
    is_open = Column(Boolean, default=True)

    amusement_park = relationship("AmusementPark", back_populates="rides")
