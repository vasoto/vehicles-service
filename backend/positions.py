from typing import List

from aioredis import Redis
from fastapi import Request

from .entities import PositionCreate

class PositionStorage:
    """ Positions store
    """
    key = "vehicles"
    def __init__(self, redis: Redis):
        self.redis = redis

    async def set(self, vehicle_id:int, position:PositionCreate):
        """ Set vehicle last position
        """
        return await self.redis.geoadd(self.key, longitude=position.longitude, latitude=position.latitude,member=vehicle_id
        )

    async def find_vehicles(self, radius:int, long:float, lat:float)->List:
        return await self.redis.georadius(self.key, longitude=long, latitude=lat, radius=radius, unit='m', with_coord=True, with_dist=True)


def get_position_storage(request: Request):
    return request.state.positions