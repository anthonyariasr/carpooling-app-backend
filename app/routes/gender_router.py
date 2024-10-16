from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import *
from app.schemas import *

gender_router = APIRouter()

@gender_router.get("", response_model=List[GenderResponse])
def get_all_genders(db: Session = Depends(get_db)):
    genders = db.query(Gender).all()
    return genders