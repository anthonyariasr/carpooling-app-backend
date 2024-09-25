from fastapi import FastAPI
from app.database import *
# from app.routes.routes import router as api_router  # Importa el router desde routes.py

app = FastAPI()

@app.get("/")
def is_running():
    return {"running": True}


@app.get("/users")
def get_users():
    users = session.query(User).all()
    users_dict = [user_to_dict(user) for user in users]
    return users_dict


# Función para convertir una instancia de User a diccionario
def user_to_dict(user):
    return {
        'id': user.id,
        'name': user.first_name,
        'lastname': user.first_surname
    }

# app.include_router(api_router)