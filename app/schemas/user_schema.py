from pydantic import BaseModel

# Esquema para crear un usuario
class UserCreate(BaseModel):
    name: str
    lastname: str

# Esquema para responder con los datos de un usuario (incluye el ID)
class UserResponse(BaseModel):
    id: int
    name: str
    lastname: str

    # Permite que Pydantic funcione con objetos SQLAlchemy
    class Config:
        orm_mode = True
