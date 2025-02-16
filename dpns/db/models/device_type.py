from dpns.db.db import Base
from sqlalchemy import Column, BigInteger, String


class DeviceType(Base):
    __tablename__ = 'device_types'
    id = Column(
        BigInteger,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    type_device = Column(String, unique=True)