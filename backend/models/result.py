

from db import Base
from sqlalchemy import Column, String, Float, Integer

class Result(Base):
    __tablename__ = "results_history"

    media_hash = Column("hash_id", String, primary_key=True)
    generation_time = Column("time_gen", Float, primary_key=True)
    score = Column("score", Float, nullable=False)
    msg = Column("message", String)

    retcode = Column("return_code", Integer)
    retfrom = Column("return_from", String)

    def __init__(self, h, t, s, msg, rf, rc = 0):
        self.media_hash = h
        self.generation_time = t
        self.score = s
        self.msg = msg
        self.retcode = rc
        self.retfrom = rf

    def __str__(self):
        return f"Hash: {self.media_hash} created: {self.generation_time}. Score: {self.score}"