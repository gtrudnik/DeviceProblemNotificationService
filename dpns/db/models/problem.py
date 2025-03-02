from dpns.db.db import Base
from sqlalchemy import Column, ForeignKey, String, DateTime, BigInteger
from datetime import datetime
from sqlalchemy.orm import relationship


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
    status = Column(String, default="active")
    date_updated_status = Column(DateTime, nullable=True)
    resolver = Column(BigInteger, ForeignKey('users.id'))
    device = Column(BigInteger, ForeignKey('devices.id'))

    authors = relationship("ProblemAuthor", back_populates="problems")
