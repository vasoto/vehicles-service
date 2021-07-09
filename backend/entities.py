from pydantic  import BaseModel

class VehicleBase(BaseModel):

    model: str
    full_name: str
    plate_number: str

class VehicleCreate(VehicleBase):
    pass


class Vehicle(VehicleBase):
    id : int
    class Config:
        orm_mode = True


class PositionBase(BaseModel):
    latitude: float
    longitude: float

class PositionCreate(PositionBase):
    vehicle_id: int

class VehiclePosition(Vehicle):
    last_position: PositionBase
    distance: float
