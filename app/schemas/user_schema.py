from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import date
from decimal import Decimal

from app.schemas.gender_schema import GenderResponse
from app.schemas.institution_schema import InstitutionBasicInfo
from app.schemas.user_type_schema import UserTypeResponse
class UserCreate(BaseModel):
    first_name: str
    first_surname: str
    identification: str
    second_name: Optional[str] = None
    second_surname: Optional[str] = None
    institutional_email: EmailStr #forma de validar un correo que tiene pydantic
    phone_number: str
    birth_date: date
    gender_id: int
    user_type_id: int
    institution_id: int
    date_registered: date
    rating: Decimal 
    total_ratings: int

class UserResponse(BaseModel):
    id: int
    first_name: str
    first_surname: str
    identification: int
    second_name: Optional[str] = None
    second_surname: Optional[str] = None
    institutional_email: EmailStr
    phone_number: str
    birth_date: date
    gender: GenderResponse
    user_type: UserTypeResponse
    institution: InstitutionBasicInfo
    date_registered: date
    rating: Decimal 
    total_ratings: int

    class Config:
        from_attributes = True

class UserBasicInfo(BaseModel):
    id: int
    name: str
    rating: Optional[Decimal] = None
