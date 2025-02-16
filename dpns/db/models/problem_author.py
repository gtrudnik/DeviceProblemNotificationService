from dpns.db.db import Base
from sqlalchemy import Column, BigInteger, ForeignKey, Integer, String


class ProblemAuthor(Base):
    __tablename__ = 'problem_authors'
    id = Column(
        BigInteger,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    author = Column(BigInteger, ForeignKey('users.id'))
    problem = Column(BigInteger, ForeignKey('problems.id'))
    grade = Column(Integer)
    comment = Column(String)
