from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
import json,time,os

Base = declarative_base()

REDIS_KEY = "qso_list"

class QSOBuilder():
    def __init__(self):
        self.callsignA = None
        self.callsignB = None
        self.rsta = None
        self.rstb = None
        self.frequency = None
        self.signal_source = None
        self.latitude = None
        self.longitude = None

    def callsignA(self, v):
        self.callsignA = v
        return self 

    def callsignB(self, v):
        self.callsignB = v
        return self 

    def rsta(self, v):
        self.rsta = v
        return self 

    def rstb(self, v):
        self.rstb = v
        return self 

    def build(self, timestamp=time.time()):
        return QSOField(
            callsignA=self.callsignA,
            callsignB=self.callsignB,
            rsta=self.rsta,
            rstb=self.rstb,
            timestamp=timestamp
        )
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

# 
    def __init__(self, callsignA, callsignB, rsta, rstb, frequency = None, signal_source = None, latitude = None, longitude = None,  timestamp = time.time()):
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

