from dpns.db.db import Base
from sqlalchemy import Column, BigInteger, ForeignKey


class DeviceAdmin(Base):
    __tablename__ = 'device_admins'
    id = Column(
        BigInteger,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    admin = Column(BigInteger, ForeignKey('users.id'))
    device = Column(BigInteger, ForeignKey('devices.id'))
