import sys
import os

# Añade el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import *
from app.base import *
from app.database import *

def test_connection():
    try:
        # Intenta conectar y obtener una conexión
        with engine.connect() as connection:
            assert connection is not None  # Asegúrate de que la conexión no sea None
            print("Conexión exitosa a la base de datos.")
    except Exception as e:
        assert False, f"Error al conectar a la base de datos: {e}"

def test_get_users():
    users = session.query(User).all()
    users_dict = [user_to_dict(user) for user in users]
    assert users_dict


def user_to_dict(user):
    return {
        'id': user.id,
        'name': user.first_name,
        'lastname': user.first_surname
    }


if __name__ == "__main__":
    test_connection()
    test_get_users()
