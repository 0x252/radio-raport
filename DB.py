from models import QSOField
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import urlparse
import os

Base = declarative_base()

class DB():
    def __init__(self):
        engine = create_engine(os.getenv('DATABASE_URL'))
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
    def close(self):
        self.session.close()

    def add(self, instance):
        self.session.add(instance)
        self.session.commit()

    def query(self, model):
        return self.session.query(model)
