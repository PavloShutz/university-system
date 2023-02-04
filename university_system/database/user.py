"""Describe user model for db"""

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String

from .db_model import base


class User(UserMixin, base):
    """Student in university."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password
