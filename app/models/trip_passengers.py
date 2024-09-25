from sqlalchemy import Table, Column, ForeignKey
from base import Base

trip_passengers = Table(
    'trip_passengers', Base.metadata, 
    Column('trip_id', ForeignKey('trip.id'), primary_key=True),
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('pickup_stop_id', ForeignKey('stop.id'))
)