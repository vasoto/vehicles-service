from fastapi import Depends, FastAPI, Request, Response
from pydantic.schema import enum_process_schema

from sqlalchemy.orm import Session

from . import crud, models, entities, endpoints
from .database import SessionLocal, engine
from .redis import init_redis
from .positions import PositionStorage
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        request.state.positions = app.state.positions
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.on_event("startup")
async def startup_event():
    app.state.redis = await init_redis()
    app.state.positions = PositionStorage(app.state.redis)


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()


app.include_router(endpoints.vehicles_router)
