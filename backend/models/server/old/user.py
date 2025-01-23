from database import Base
from sqlalchemy import Column, String

class User(Base):
    __tablename__ = "users"

    uid = Column("uid", String, primary_key=True)
    firstName = Column("first_name", String)
    lastName = Column("last_name", String)
    email = Column("email", String)
    password = Column("password", String)


    def __init__(self, uid, firstName, lastName, email, password):
        self.uid = uid
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password

    def __str__(self):
        return f"{self.firstName} {self.lastName}: {self.email}"


