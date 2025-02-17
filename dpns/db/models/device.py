from dpns.db.db import Base
from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey
from datetime import datetime


class Device(Base):
    __tablename__ = 'devices'
    id = Column(
        BigInteger,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    name = Column(String)
    type_device = Column(BigInteger, ForeignKey('device_types.id'), nullable=True)
    description = Column(String)
    building = Column(String)
    floor = Column(Integer)
    room = Column(String)
    location_description = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)