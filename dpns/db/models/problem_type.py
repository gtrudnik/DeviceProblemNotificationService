from dpns.db.db import Base
from sqlalchemy import Column, BigInteger, String, ForeignKey


class ProblemType(Base):
    __tablename__ = 'problem_types'
    id = Column(
        BigInteger,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    type_device = Column(BigInteger, ForeignKey('device_types.id'))
    name_problem = Column(String)
    description = Column(String)