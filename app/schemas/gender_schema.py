from pydantic import BaseModel
from typing import Optional

class GenderCreate(BaseModel):
    name: str

class GenderResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
