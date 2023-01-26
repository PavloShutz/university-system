"""Describe student model for db"""


from sqlalchemy import Column, Integer, String, ForeignKey

from .db_model import base


class Student(base):
    """Student in university."""

    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    surname = Column(String)
    name = Column(String)
    age = Column(Integer)
    address = Column(String)
    group = Column(Integer, ForeignKey('groups.id'))

    def __init__(self, surname, name, age, address, group):
        self.surname = surname
        self.name = name
        self.age = age
        self.address = address
        self.group = group

    def __repr__(self):
        return f"<Student '{self.surname} {self.name}'>"

    def __str__(self):
        return f"{self.name} {self.surname}"
