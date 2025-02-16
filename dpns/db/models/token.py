from dpns.db.db import Base
from sqlalchemy import Column, String, Integer


class Token(Base):
    __tablename__ = 'tokens'
    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    name = Column(String, nullable=False)
    token = Column(
        String,
        nullable=False,
        primary_key=True,
        unique=True,
    )
    role = Column(String, nullable=False)
