from app.settings import engine

def test_connection():
    try:
        # Intenta conectar y obtener una conexión
        with engine.connect() as connection:
            print("Conexión exitosa a la base de datos.")
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")

if __name__ == "__main__":
    test_connection()



# Prueba conexión:
# python test_connection.py
