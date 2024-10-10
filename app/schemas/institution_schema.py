from pydantic import BaseModel
from typing import Optional

class InstitutionCreate(BaseModel):
    name: str
    description: Optional[str]
    address: str

class InstitutionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    address: str

    class Config:
        orm_mode = True
