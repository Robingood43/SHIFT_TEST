from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR, FLOAT, DATE
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(255), unique=True, nullable=False)
    hashed_password = Column(VARCHAR(255), nullable=False)


class SalaryDetails(Base):
    __tablename__ = 'salary_details'
    id = Column(INTEGER, ForeignKey("users.id"), primary_key=True)
    salary = Column(FLOAT, nullable=False)
    next_raise = Column(DATE, nullable=False)
