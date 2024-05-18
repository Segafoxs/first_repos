from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


class User(BaseModel):
    username: str
    password: str

class Person(Base):
    __tablename__ = "Workers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    login = Column(String)
    password = Column(String)
