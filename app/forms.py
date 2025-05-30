from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, Length
import sqlalchemy as sa
from app import db
from app.models import User
from wtforms.widgets import TextArea

from email_validator import validate_email, EmailNotValidError

#the form used by the signup function in the routes file
class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    #checks if the email already exists in the database, doesnt allow signup if so
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')

#the form used by the login function in the routes file
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

#the form used by the feedback submission box in the website
class FeedbackForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)], widget=TextArea())
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)], widget=TextArea())
    email = StringField('Email', validators=[DataRequired(), Length(max=100)], widget=TextArea())
    subject = StringField('Subject', validators=[DataRequired(), Length(max=50)], widget=TextArea())
    message = StringField('Message', validators=[DataRequired(), Length(max=245)], widget=TextArea())
    submit = SubmitField('Submit')

    #checks if the email is valid
    def validate_email(self, email):
        try:
            emailinfo = validate_email(email, check_deliverability=False)
            email = emailinfo.normalized
        except EmailNotValidError as e:
            raise ValidationError(e)
         

#form used in the forgot password page's functionality
class PasswordChange(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Confirm')

#form used in account detail editing functionality
class AccountEditForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional(), Length(max=30)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=30)])
    email = StringField('Email', validators=[Optional()])
    old_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=8)])
    #confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Save Changes')
    delete_account = SubmitField('Delete Account', render_kw={
        "class": "delete",
        "onclick": "return confirm('Are you sure you want to delete your account? This action is irreversible!');"
    })

#form for user uploaded images
class UploadImage(FlaskForm):
    file = FileField('File', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'JPG or PNG images only.')])
    submit = SubmitField('Submit')