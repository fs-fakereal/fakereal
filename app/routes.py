from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from app import app
from app import db
from app.forms import SignupForm
from app.forms import LoginForm
from app.models import User
import sqlalchemy as sa

#this file tells flask where to route the website's traffic
#backend routing logic for site urls
#routes to home page
@app.route('/')
@app.route('/home')
#@login_required
def index():
    return render_template('home-page.html', title='Home')

#route to the about page
@app.route('/about')
def about():
    return render_template('about.html', title='About')

#route to the login page
#uses a form defined in another file, and cross checks the form submission data in the database
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_pass(form.password.data):
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('login-page.html', title='Login', form = form)

#route to the signup page
#uses similar methods to the lgoin function
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        user.set_pass(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup-page.html', title='Signup', form = form)

#logs the user out, removing their authentication
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

#routes to the scan results page
@app.route('/result')
@login_required
def result():
    return render_template('result.html', title='Result')

#route to the page that allows users to scan photos
@app.route('/scan')
@login_required
def scan():
    return render_template('scan-image.html', title='Scan')

#route to the page that allows users to upload
@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html', title='Upload')

#route to dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

#routes to the user account detail editing page
@app.route('/edit')
@login_required
def user_edit():
    return render_template('user-edit.html', title='User Edit')