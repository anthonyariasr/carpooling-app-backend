from sqlalchemy import DDL
from app.database import *
from app.tec_db import setup_tec_db, delete_all_data_tec


def delete_all_data():
    session.query(trip_passengers).delete()
    session.query(Trip).delete()
    session.query(Stop).delete()
    session.query(Vehicle).delete()
    session.query(User).delete()
    session.query(Institution).delete()
    session.query(Brand).delete()
    session.query(UserType).delete()
    session.query(VehicleType).delete()
    session.query(Gender).delete()
    session.query(TripStatus).delete()
    
    # Confirmar los cambios en la base de datos
    session.commit()

    ddl_statements = [
        DDL("ALTER SEQUENCE trip_id_seq RESTART WITH 1;"),
        DDL("ALTER SEQUENCE stop_id_seq RESTART WITH 1;"),
        DDL("ALTER SEQUENCE vehicle_id_seq RESTART WITH 1;"),
        DDL("ALTER SEQUENCE user_id_seq RESTART WITH 1;"),
        DDL("ALTER SEQUENCE institution_id_seq RESTART WITH 1;"),
        DDL("ALTER SEQUENCE brand_id_seq RESTART WITH 1;"),
        DDL("ALTER SEQUENCE user_type_id_seq RESTART WITH 1;"),
        DDL("ALTER SEQUENCE vehicle_type_id_seq RESTART WITH 1;"),
        DDL("ALTER SEQUENCE gender_id_seq RESTART WITH 1;"),
        DDL("ALTER SEQUENCE gender_id_seq RESTART WITH 1;")
    ]

    # Ejecutar cada comando DDL
    for ddl in ddl_statements:
        session.execute(ddl)
    session.commit()

delete_all_data()

delete_all_data_tec()