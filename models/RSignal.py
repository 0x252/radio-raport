from sqlalchemy import create_engine, Column, Integer, String, Float, Decimal
from sqlalchemy.ext.declarative import declarative_base
import json,time,os
Base = declarative_base()

class RSignal(Base):
    id = Column(Integer, primary_key=True, autoincrement=True) 
    frequency = Column(Decimal, nullable=False)
    timestamp = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    signalStrength = Column(Float, nullable=True)
    modulationType = Column(String, nullable=False)
    bandwidth = Column(Float, nullable=True)
    antenna = Column(String, nullable=True)

database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set.")

engine = create_engine(os.getenv('DATABASE_URL'))
Base.metadata.create_all(engine)
