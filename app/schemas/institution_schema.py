from pydantic import BaseModel
from typing import Optional

class InstitutionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    acronym: Optional[str] = None

class InstitutionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    address: str
    acronym: Optional[str] = None

    class Config:
        from_attributes = True

class InstitutionBasicInfo(BaseModel):
    id: int
    name: str
    acronym: Optional[str] = None
