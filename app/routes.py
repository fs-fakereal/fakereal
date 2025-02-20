import hashlib
import os
import time

import sqlalchemy as sa

from app import app, db, mse
from app.forms import LoginForm, SignupForm
from app.models import User
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.orm import sessionmaker

from werkzeug.utils import secure_filename

#--Constants for Model--#
# TODO(liam): session is not working
Session = sessionmaker(bind=db)
s = Session()
MODEL_DEBUG_PRINT = True
DATA_UPLOAD_FOLDER = './data'
DATA_UPLOAD_EXTENSIONS_WHITELIST = { 'png', 'jpg', 'jpeg' }
recent_results = {}
#-----------------------#

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

@app.route('/upload', methods=["POST"])
def _file_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return {"error": "no file found"}, 400

        try:
            # NOTE(liam): file processing section
            file = request.files['file']
            filename = secure_filename(file.filename)
            ext = mse.file_get_extension(filename)

            if ext not in DATA_UPLOAD_EXTENSIONS_WHITELIST:
                return {"error": "file extension blocked"}, 400

            # NOTE(liam): saves file temporarily
            bufpath = os.path.join(DATA_UPLOAD_FOLDER, f"{time.time()}.{ext}")
            file.save(bufpath)

            # NOTE(liam): file.read() and file.save() is a blocking process,
            # so basically I can't run either one after the other.
            # Idk how else to fix this than what I did here.
            with open(bufpath, "rb") as bf:
                contents = bf.read()
                hash = hashlib.sha256(contents).hexdigest()
                filepath = os.path.join(DATA_UPLOAD_FOLDER, f"{hash}.{ext}")

            # TODO(liam): this is definitely not efficient,
            # but it works, so good enough for now.
            if not (os.path.isfile(filepath)):
                os.rename(bufpath, filepath)
            else:
                os.remove(bufpath)

            result = ""
            if hash in recent_results.keys():
                if MODEL_DEBUG_PRINT:
                    print("INFO: Hash found. Restoring previous result.")
                result = recent_results[hash]
            else:
                if MODEL_DEBUG_PRINT:
                    print("INFO: Sending image to model.")

                result = mse.parse_check(mse.check_media(filepath))
                recent_results[hash] = result

            mse.push_results(s, result, hash)

        except Exception as e:
            print(f"ERROR: {e}")
            return {"error": f"Error processing file: {str(e)}"}, 500

        finally:
            if MODEL_DEBUG_PRINT:
                print("INFO: Finished processing. Returning to client.")
            file.close()

        return { "hash": hash, "result": result }
