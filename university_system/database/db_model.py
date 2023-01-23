from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db = create_engine('sqlite:///app.db', connect_args={'check_same_thread': False})
Session = sessionmaker(bind=db)
session = Session()
base = declarative_base()


def create_db():
    base.metadata.create_all(db)
