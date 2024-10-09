from pydantic import BaseModel

class UserTypeCreate(BaseModel):
    name: str

class UserTypeResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
