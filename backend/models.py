""" SQLAlchemy models
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Float

from .database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, unique=True, index=True)
    model = Column(String)
    full_name = Column(String)
    positions = relationship("Position", back_populates="vehicle")

class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    longitude = Column(Float)
    latitude = Column(Float)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    vehicle = relationship("Vehicle", back_populates="positions")