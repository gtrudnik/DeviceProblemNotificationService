from dpns.db.db import Base
from sqlalchemy import Column, BigInteger, String


class DeviceProblems(Base):
    __tablename__ = 'problems'
    id = Column(
        BigInteger,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    type_device = Column(String)
    name_problem = Column(String)
    description = Column(String)