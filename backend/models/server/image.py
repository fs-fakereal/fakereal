from database import Base
from sqlalchemy import Column, String

class Image(Base):
    __tablename__ = "images"

    uid = Column("uid", String, primary_key=True)
    url = Column("url", String)
    userUid = Column("user_Uid", String)

    def __init__(self, uid, userUid, url):
        self.uid = uid
        self.userUid = userUid
        self.url = url

    def __str__(self):
        return f"Uid: {self.uid} of {self.userUid}; URL {self.url}"
