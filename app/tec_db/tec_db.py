from sqlalchemy import DDL, Column, String, create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os


load_dotenv()

# Leer la variable de entorno DATABASE_URL
DATABASE_TEC = os.getenv("DATABASE_TEC")

Base2 = declarative_base()

class User(Base2):
    __tablename__  = 'user_tec'
    email = Column(String, primary_key=True)
    password = Column(String)

engine = create_engine(DATABASE_TEC, echo=False)
Base2.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_user_tec (email: str, password: str):
    user = session.query(User).filter(User.email == email).first()
    if user == None:
        return False
    if user.password == password:
        return True
    return False

def setup_tec_db():
    # Lista de 200 nombres únicos
    nombres = [
        'Carlos', 'Ana', 'Luis', 'Maria', 'Jorge', 'Sofia', 'Raul', 'Gabriela', 'Pedro', 'Lucia',
        'Andres', 'Laura', 'David', 'Marta', 'Juan', 'Elena', 'Roberto', 'Patricia', 'Alberto', 'Daniela',
        'Fernando', 'Isabel', 'Jose', 'Beatriz', 'Ricardo', 'Carmen', 'Victor', 'Angela', 'Francisco', 'Adriana',
        'Cristian', 'Veronica', 'Miguel', 'Sandra', 'Enrique', 'Julia', 'Oscar', 'Paula', 'Eduardo', 'Claudia',
        'Manuel', 'Monica', 'Hector', 'Rosa', 'Felipe', 'Irene', 'Sebastian', 'Natalia', 'Gonzalo', 'Alejandra',
        'Ramiro', 'Noelia', 'Sergio', 'Lorena', 'Marcos', 'Esther', 'Rafael', 'Valeria', 'Guillermo', 'Eva',
        'Pablo', 'Ines', 'Esteban', 'Vanessa', 'Salvador', 'Silvia', 'Rodrigo', 'Alicia', 'Nicolas', 'Cristina',
        'Julio', 'Miriam', 'Agustin', 'Rebeca', 'Leandro', 'Teresa', 'Alvaro', 'Olga', 'Bruno', 'Yolanda',
        'Emilio', 'Sonia', 'Federico', 'Nuria', 'Hugo', 'Tamara']

    # Elimina los nombres duplicados
    nombres = list(set(nombres))

    users_tec = []

    for nombre in nombres:
        email = f'{nombre.lower()}@estudiantec.cr'
        password = nombre.lower()

        # Verificar si ya existe un usuario con el mismo correo
        existing_user = session.query(User).filter(User.email == email).first()
        if not existing_user:
            user_tec = User(
                email=email,
                password=password
            )
            users_tec.append(user_tec)

    session.add_all(users_tec)
    session.commit()
    print('Usuarios del TEC creados exitosamente')

def delete_all_data_tec():
    session.query(User).delete()
    session.commit()
    session.commit()
