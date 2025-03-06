from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app import login
from flask_login import UserMixin
import uuid

#models are defined here for backend to database interaction
#every table used in our database should have a model equivalent here
#usermixin is for authentication purposes

class User(UserMixin, db.Model):    
    __tablename__ = "users"
    id: so.Mapped[Optional[int]] = so.mapped_column(primary_key=True) #consider uuids
    first_name: so.Mapped[str] = so.mapped_column(sa.String(50), index=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(50), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    created_at: so.Mapped[Optional[datetime]] = so.mapped_column(index=True, default=datetime.now())

    #sets the plaintext password given by the user in the form to a hash
    def set_pass(self, password):
        self.password_hash = generate_password_hash(password)

    #checks the password hash in the database with the plaintext password from the user
    def check_pass(self, password):
        return check_password_hash(self.password_hash, password)
    
    #needed to have a logged in user session
    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

    #writes output for debug
    def __repr__(self):
        return '<User: {}>'.format(self.first_name)

class Feedback(db.Model):
    __tablename__ = "support-feedback"
    id: so.Mapped[Optional[int]] = so.mapped_column(primary_key=True) #consider uuids
    created_at: so.Mapped[Optional[datetime]] = so.mapped_column(index=True, default=datetime.now())
    first_name: so.Mapped[str] = so.mapped_column(sa.String(50), index=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(50), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    subject : so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    message: so.Mapped[str] = so.mapped_column(sa.String, index=True)