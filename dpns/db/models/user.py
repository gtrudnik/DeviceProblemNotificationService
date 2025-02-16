from dpns.db.db import Base
from sqlalchemy import Column, String, DateTime, BigInteger
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(
        BigInteger,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    login = Column(String)
    tg_id = Column(BigInteger)
    role = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)