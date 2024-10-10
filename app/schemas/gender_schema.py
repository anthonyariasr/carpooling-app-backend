from pydantic import BaseModel
from typing import Optional

class GenderCreate(BaseModel):
    name: str
    description: Optional[str] 

class GenderResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] 

    class Config:
        orm_mode = True
