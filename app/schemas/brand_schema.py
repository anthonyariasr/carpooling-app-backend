from pydantic import BaseModel
from typing import Optional

class BrandCreate(BaseModel):
    name: str

class BrandResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
