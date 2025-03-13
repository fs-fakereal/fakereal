import hashlib
import json
import os
import time

import requests

import sqlalchemy as sa

from app import app, db, mse
from app.forms import (
    AccountEditForm,
    FeedbackForm,
    LoginForm,
    PasswordChange,
    SignupForm,
)
from app.models import Feedback, User
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from werkzeug.utils import secure_filename


#--Constants for Model--#
MODEL_DEBUG_PRINT = True
DATA_UPLOAD_FOLDER = 'models/data/user'
DATA_UPLOAD_EXTENSIONS_WHITELIST = { 'png', 'jpg', 'jpeg' }
JSON_FOLDER = 'app/static/json'

# TODO(liam): session is not working
Session = sessionmaker(bind=db)
s = Session()
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
@app.route('/about', methods=['GET', 'POST'])
def about():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(feedback)
        db.session.commit()
        flash('Your message was submitted!', 'success')
        return redirect(url_for('about') + '#support')
    return render_template('about.html', title='About', form=form)

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

#route to logged in version of home page
@app.route('/logged-in/home-page')
@login_required
def loggedHomePage():
    return render_template('logged-in/home-page.html', title='LoggedHome')

#route to logged in version of about page
@app.route('/logged-in/about')
@login_required
def loggedAbout():
    return render_template('logged-in/about.html', title='LoggedAbout')

#route to the signup page
#uses similar methods to the login function
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignupForm()
    if form.validate_on_submit():
        try:
            existing_user = User.query.filter_by(email=form.email.data).first()
            #Checks here if email is already in use. If it is throws an error
            if existing_user:
                flash('Email already in use. Please use a different email.', 'error')
            #If email is not in use goes here. User will be able to create an account
            else:
                user = User(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data
                )
                user.set_pass(form.password.data)
                db.session.add(user)
                db.session.commit()
                # Pass success message and redirect URL to the template
                return render_template('signup-page.html', title='Signup', form=form, success_message='Account created successfully! Redirecting to login page...', redirect_url=url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'error')
            app.logger.error(f"Error during signup: {e}")

    return render_template('signup-page.html', title='Signup', form=form)


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
@app.route('/scan', methods=['GET', 'POST'])
@login_required
def scan():
    return render_template('scan-image.html', title='Scan')

#route to the page that allows users to upload
@app.route('/upload', methods=['GET'])
@login_required
def upload():
    return render_template('upload.html', title='Upload')

#route to dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

#routes to the user account detail editing page
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def user_edit():
    form = AccountEditForm()
    if form.validate_on_submit():
        updated = False

        if form.delete_account.data:
            db.session.delete(current_user)
            db.session.commit()
            logout_user()  # Logs the user out
            flash("Your account has been deleted.", "danger")
            return redirect(url_for('index'))

        # Update only if field is not empty
        if form.first_name.data:
            current_user.first_name = form.first_name.data
            updated = True
        if form.last_name.data:
            current_user.last_name = form.last_name.data
            updated = True
        if form.email.data:
            current_user.email = form.email.data
            updated = True
        if form.new_password.data:
            if not form.old_password.data:
                flash("You must enter your current password to set a new one.", "warning")
                return redirect(url_for('user_edit'))
            # Verify current password
            if not check_password_hash(current_user.password_hash, form.old_password.data):
                flash("Incorrect current password.", "danger")
                return redirect(url_for('user_edit'))
            # Hash and update new password
            current_user.password_hash = generate_password_hash(form.new_password.data)
            updated = True
        if updated:
            db.session.commit()
            flash("Account updated successfully!", "success")
        else:
            flash("No changes made.", "info")

        return redirect(url_for('user_edit'))
    return render_template('user-edit.html', title='User Edit', form=form)

#routes to the forgot password page
@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    form = PasswordChange()
    return render_template('forgot-password.html', title='Forgot Password', form=form)

# routes to the feb-articles
@app.route('/feb-article')
def feb_article():
    return render_template('articles/feb-article-list.html')

# routes to the empty_cab
@app.route('/empty_cab')
def empty_cab():
    return render_template('articles/empty_cab.html')

# NOTE(liam): gets existing news or get a new one if not existing, or if it's
# been 30 days since the news was created.
@app.route('/news', methods=['GET'])
def get_news():
    if request.method == 'GET':
        json_folder_dir = os.path.join(os.getcwd(), JSON_FOLDER)
        filepath = os.path.join(json_folder_dir, 'news.json')

        time_now = time.time()
        time_created = 0

        dat: dict = {}

        try:
            if (not os.path.exists(json_folder_dir)):
                os.makedirs(json_folder_dir, exist_ok = True)

            if (os.path.exists(filepath)):
                time_created = os.path.getctime(filepath)

            # NOTE(liam): approximate 30 days in seconds
            if (time_created == 0 or time_now - time_created > 2_592_000):

                # NOTE(liam): make fetch here
                news_url = f"https://newsapi.org/v2/everything?q=Deepfake&language=en&apiKey={os.getenv('NEWS_SECRET')}"

                response = requests.get(news_url)
                dat = response.json()

                with open(filepath, "w", encoding = 'utf8') as json_file:
                    json.dump(dat, json_file, ensure_ascii = True)

            else:
                with open(filepath, "r") as json_file:
                    dat = json.load(json_file)
        except Exception as e:
            print(e)

        return dat

@app.route('/upload', methods=["POST"])
def _file_upload():
    if request.method == 'POST':
        # NOTE(liam): route to post req for upload
        if 'file' not in request.files:
            return {"error": "no file found"}, 400

        try:
            # NOTE(liam): file processing section
            file = request.files['file']
            filename = secure_filename(file.filename)
            ext = mse.file_get_extension(filename)
            model_id = request.args.get('model', None) or 'genai'

            data_dir = os.path.join(os.getcwd(), DATA_UPLOAD_FOLDER)

            if not os.path.exists(data_dir):
                os.makedirs(data_dir, exist_ok=True)

            if ext not in DATA_UPLOAD_EXTENSIONS_WHITELIST:
                return {"error": "file extension blocked"}, 400

            # NOTE(liam): saves file temporarily
            bufpath = os.path.join(data_dir, f"{time.time()}.{ext}")
            file.save(bufpath)

            with open(bufpath, "rb") as bf:
                contents = bf.read()
                hash = hashlib.sha256(contents).hexdigest()
                filepath = os.path.join(data_dir, f"{hash}.{ext}")

            if (os.path.isfile(filepath)):
                os.remove(filepath)

            os.rename(bufpath, filepath)

            # check existing hash
            result = ""
            if hash in recent_results.keys():
                if MODEL_DEBUG_PRINT:
                    print("INFO: Hash found. Restoring previous result.")
                result = recent_results[hash]
                if result['model'] != model_id:
                    if MODEL_DEBUG_PRINT:
                        print("INFO: Model mismatch. Sending image to model anyways.")
                    result = mse.prediction(filepath, { 'model_id' : model_id })
                    recent_results[hash] = result

            else:
                if MODEL_DEBUG_PRINT:
                    print("INFO: Sending image to model.")

                result = mse.prediction(filepath, { 'model_id' : model_id })
                recent_results[hash] = result

            # mse.push_results(s, result, hash)
            # s.flush()

        except Exception as e:
            print(f"ERROR: {e}")
            return {"error": f"Error processing: {str(e)}"}, 500

        finally:
            if MODEL_DEBUG_PRINT:
                print("INFO: Finished processing. Returning to client.")
            file.close()

        return { "hash": hash, "result": result }
