import json
REDIS_KEY = "qso_list"

class QSOField:    
    def __init__(self, callsignA, callsignB, rsta, rstb):
     self.callsignA = callsignA
     self.callsignB = callsignB
     self.rsta = rsta
     self.rstb = rstb
     self.timestamp = time.time()
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
