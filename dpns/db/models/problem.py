from dpns.db.db import Base
from sqlalchemy import Column, ForeignKey, String, DateTime, BigInteger
from datetime import datetime


class Problem(Base):
    __tablename__ = 'problems'
    id = Column(
        BigInteger,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    type_problem = Column(String)
    description = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_resolved = Column(DateTime, nullable=True)
    status = Column(String)
    resolver = Column(BigInteger, ForeignKey('users.id'))
    device = Column(BigInteger, ForeignKey('devices.id'))
