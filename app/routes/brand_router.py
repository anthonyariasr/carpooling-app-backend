from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import *
from app.schemas import *

brand_router = APIRouter()

@brand_router.get("", response_model=List[BrandResponse])
def get_all_brands(db: Session = Depends(get_db)):
    brands = db.query(Brand).all()
    return brands