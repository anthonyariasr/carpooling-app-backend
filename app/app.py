from typing import List, Optional
from datetime import date, time
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session, aliased
from app.database import *
from app.schemas import *

from app.routes import *
# import app.routes import user_router

app = FastAPI()

app.include_router(trip_router, prefix="/trips")
app.include_router(trip_status_router, prefix="/trip_statuses")
app.include_router(vehicle_type_router, prefix="/vehicle_types")
app.include_router(brand_router, prefix="/brands")
app.include_router(gender_router, prefix="/genders")
app.include_router(institution_router, prefix="/institutions")
app.include_router(statistic_router, prefix="/statistic")


@app.get("/")
def is_running():
    return {"running": True}
