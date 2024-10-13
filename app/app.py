from typing import List, Optional
from datetime import date, time
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session, aliased
from app.database import *
from app.schemas import *

from app.routes import trip_router 
# import app.routes import user_router

app = FastAPI()

app.include_router(trip_router, prefix="/trips")

@app.get("/")
def is_running():
    return {"running": True}
