
from datetime import datetime
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
# from sqlalchemy import Column, Float, Integer, String

class Result(db.Model):
    __tablename__ = "results_history"

    # media_hash = Column("hash_id", String, primary_key=True)
    # generation_time = Column("time_gen", Float, primary_key=True)
    # score = Column("score", Float, nullable=False)
    # msg = Column("message", String)
    #
    # retcode = Column("return_code", Integer)
    # retfrom = Column("return_from", String)

    media_hash: so.Mapped[str] = so.mapped_column(sa.String, primary_key=True)
    generation_time: so.Mapped[str] = so.mapped_column(sa.String, default=datetime.now(), primary_key=True)
    score: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    msg: so.Mapped[Optional[str]] = so.mapped_column(sa.String)

    retcode: so.Mapped[int] = so.mapped_column(sa.Integer)
    retfrom: so.Mapped[str] = so.mapped_column(sa.String)

    def __init__(self, h, t, s, msg, rf, rc = 0):
        self.media_hash = h
        self.generation_time = t
        self.score = s
        self.msg = msg
        self.retcode = rc
        self.retfrom = rf

    def __str__(self):
        return f"Hash: {self.media_hash} created: {self.generation_time}. Score: {self.score}"
