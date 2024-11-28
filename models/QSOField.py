from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
import json,time,os

Base = declarative_base()

REDIS_KEY = "qso_list"

class QSOField(Base):
    __tablename__ = 'qso'  
# For PSQL
    id = Column(Integer, primary_key=True, autoincrement=True) 
    callsignA = Column(String, nullable=False)
    callsignB = Column(String, nullable=False)
    rsta = Column(String, nullable=False)
    rstb = Column(String, nullable=False)
    timestamp = Column(Float, nullable=False)
# 
    def __init__(self, callsignA, callsignB, rsta, rstb, timestamp = time.time()):
# For redis
     self.callsignA = callsignA
     self.callsignB = callsignB
     self.rsta = rsta
     self.rstb = rstb
     self.timestamp = timestamp

    def to_dict(self):
        return {
            "callsignA": self.callsignA,
            "callsignB": self.callsignB,
            "rsta": self.rsta,
            "rstb": self.rstb,
            "timestamp": self.timestamp
        }
    @property
    def json(self):
       return self.to_json()
    
    def to_json(self):
        return json.dumps(self.to_dict())

engine = create_engine(os.getenv('DATABASE_URL'))
Base.metadata.create_all(engine)

