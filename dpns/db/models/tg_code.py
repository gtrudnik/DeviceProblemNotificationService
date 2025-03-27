from dpns.db.db import Base
from sqlalchemy import Column, String, DateTime, BigInteger, Integer, ForeignKey
from datetime import datetime


class TgCode(Base):
    __tablename__ = 'tg_codes'
    id = Column(
        BigInteger,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    tg_id = Column(BigInteger, ForeignKey('tg_chats.tg_id'), unique=True)
    code = Column(Integer)
    attempts = Column(Integer, default=3)
    date_created = Column(DateTime, default=datetime.utcnow)
