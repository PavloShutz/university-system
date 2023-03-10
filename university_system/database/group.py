"""Describe group model for db"""


from sqlalchemy import Column, Integer, String

from .db_model import base


class Group(base):
    """Group of students in university class."""

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    group_name = Column(String)

    def __init__(self, group_name):
        self.group_name = group_name
