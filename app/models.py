import uuid
from datetime import datetime, timezone
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

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

#model for the feedback table in the database
class Feedback(db.Model):
    __tablename__ = "support-feedback"
    id: so.Mapped[Optional[int]] = so.mapped_column(primary_key=True) #consider uuids
    created_at: so.Mapped[Optional[datetime]] = so.mapped_column(index=True, default=datetime.now())
    first_name: so.Mapped[str] = so.mapped_column(sa.String(50), index=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(50), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    subject : so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    message: so.Mapped[str] = so.mapped_column(sa.String, index=True)

class ScanResult(db.Model):
    __tablename__ = "scan_results"
    #__table_args__ = {'extend_existing': True}
    #id: so.Mapped[Optional[int]] = so.mapped_column(primary_key=True)
    hash: so.Mapped[str] = so.mapped_column("hash", sa.String(64), primary_key=True, unique=True, index=True, nullable=False)
    time: so.Mapped[float] = so.mapped_column("time", sa.Float, primary_key=True, nullable=False)
    explanation: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    model: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)
    score: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    status_message: so.Mapped[str] = so.mapped_column("message", sa.String(255), nullable=False)
    status_code: so.Mapped[int] = so.mapped_column("return_code", sa.Integer, nullable=False)
    status_from: so.Mapped[str] = so.mapped_column("return_from", sa.String(50), nullable=False)
    user_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("users.id"))

    def __init__(self, hash, time, explanation, model, score, status_message, status_from, status_code = 0, user_id = 0):
        self.hash = hash
        self.time = time
        self.explanation = explanation
        self.model = model
        self.score = score
        self.status_message = status_message
        self.status_from = status_from
        self.status_code = status_code
        self.user_id = user_id

    def __str__(self):
        ret_str = f"Hash: {self.hash} created: {self.time}. Score: {self.score}"
        if self.user_id:
            ret_str += f"\nUser: {self.user_id}"

        return ret_str
