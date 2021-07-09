from typing import Optional
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from pydantic.types import NoneBytes
from sqlalchemy.orm import Session

from .crud import get_vehicle_by_id, get_vehicle_by_plate, create_vehicle

from .database import get_db
from .entities import PositionBase, VehicleCreate, Vehicle, VehiclePosition
from .positions import get_position_storage, PositionStorage


vehicles_router = APIRouter()


@vehicles_router.get("/vehicles/{vehicle_id}", response_model=Vehicle)
async def vehicle_by_id(vehicle_id:int, db:Session= Depends(get_db) ):
    vehicle = get_vehicle_by_id(db, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404,
                            detail=f"Vehicle with id={vehicle_id} not found.")
    return vehicle

#,
@vehicles_router.post("/vehicles", response_model=Vehicle)
async def add_vehicle(vehicle_data:VehicleCreate, db:Session= Depends(get_db) ):
    # Check if exists
    vehicle = get_vehicle_by_plate(db, vehicle_data.plate_number)
    if vehicle:
        raise HTTPException(status_code=400, detail=f"Vehicle with plate number {vehicle_data.plate_number} already exists")
    return create_vehicle(db, vehicle_data=vehicle_data)

@vehicles_router.post("/vehicles/{vehicle_id}/position")
async def add_position(vehicle_id: int,
                       position_data: PositionBase,
                       storage: PositionStorage = Depends(get_position_storage)):
    """ Add position
    """
    result = await storage.set(vehicle_id=vehicle_id, position=position_data)
    print(result)



@vehicles_router.get("/vehicles")
async def find_vehicle(
    plate_number: Optional[str] = None,
    longitude: Optional[float] = None,
    latitude: Optional[float] = None,
    nearby_radius: Optional[int] = None,
    db: Session = Depends(get_db),
    storage: PositionStorage = Depends(get_position_storage)):
    if plate_number:
        if latitude or longitude:
            raise HTTPException(status_code=400, detail="Longitude or latitude specified along with plate number")
        vehicle = get_vehicle_by_plate(db, plate_number=plate_number)
        if vehicle is None:
            raise HTTPException(
                status_code=404,
                detail=f"Vehicle with plate_number={plate_number} not found.")
    elif latitude and longitude and nearby_radius:
        result = await storage.find_vehicles(radius=nearby_radius,
                                       long=longitude,
                                       lat=latitude)
        print(result)
        response = []
        for record in result:
            # fetch vehicle data fro the database
            vehicle = get_vehicle_by_id(db, int(record.member))
            if vehicle is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Vehicle with id={record.member} not found.")
            # Get position info
            pos = PositionBase(longitude=record.coord.longitude, latitude=record.coord.latitude)
            # Get distance info
            dist = record.dist
            # Create response object
            v = VehiclePosition(
                plate_number=vehicle.plate_number,
                model=vehicle.model,
                id=vehicle.id,
                full_name=vehicle.full_name,
                distance=dist,
                last_position=pos,
            )
            response.append(v)
        return response
