from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import InstitutionCreate, InstitutionResponse
from app.models import Institution

institution_router = APIRouter()

# Obtener la información de una institución por ID
@institution_router.get("/{institution_id}", response_model=InstitutionResponse)
def get_institution(institution_id: int, db: Session = Depends(get_db)):
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    if not institution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found")
    return institution

# Obtener la lista de todas las instituciones
@institution_router.get("/all-institutions", response_model=List[InstitutionResponse])
def get_all_institutions(db: Session = Depends(get_db)):
    institutions = db.query(Institution).all()
    return institutions

# Registrar una nueva institución
@institution_router.post("", response_model=InstitutionResponse, status_code=status.HTTP_201_CREATED)
def create_institution(institution: InstitutionCreate, db: Session = Depends(get_db)):
    new_institution = Institution(**institution.dict())
    db.add(new_institution)
    db.commit()
    db.refresh(new_institution)
    return new_institution


# Eliminar una institución por ID 
# WARNING! CASCADE DELETE USERS
@institution_router.delete("/{institution_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_institution(institution_id: int, db: Session = Depends(get_db)):
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    
    if not institution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found")
    
    # Elimina la institución (y todos los usuarios asociados por cascada)
    db.delete(institution)
    db.commit()
    return {"message": "Institution and associated users deleted successfully"}