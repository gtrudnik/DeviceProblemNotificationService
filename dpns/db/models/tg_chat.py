from dpns.db.db import Base
from sqlalchemy import Column, String, DateTime, BigInteger
from datetime import datetime


class TgChat(Base):
    __tablename__ = 'tg_chats'
    id = Column(
        BigInteger,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    tg_id = Column(BigInteger, unique=True)
    stage = Column(String)
    device_id = Column(BigInteger)
    problem_type = Column(String)
    description = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)
