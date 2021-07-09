from functools import lru_cache
import os

from pydantic import BaseSettings, AnyUrl


class Config(BaseSettings):
    redis_url: AnyUrl
    redis_db: int = 0

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_config():
    return Config()