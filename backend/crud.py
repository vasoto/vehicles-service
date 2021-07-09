from sqlalchemy.orm import Session

from . import entities, models


def get_vehicle_by_plate(db: Session, plate_number: str):
    """ Get vehicle by ID
    """
    return db.query(
        models.Vehicle).filter(models.Vehicle.plate_number == plate_number).first()


def get_vehicle_by_id(db: Session, vehicle_id:int):
    """ Get vehicle by ID
    """
    return db.query(models.Vehicle).filter(models.Vehicle.id==vehicle_id).first()

def create_vehicle(db: Session, vehicle_data: entities.VehicleCreate) -> models.Vehicle:
    """ Create new vehicle
    """
    vehicle = models.Vehicle(plate_number=vehicle_data.plate_number, model=vehicle_data.model, full_name=vehicle_data.full_name)
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle
