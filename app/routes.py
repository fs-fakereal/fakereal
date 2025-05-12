import hashlib
import json
import logging
import os
import shutil
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
    UploadImage,
)
from app.models import Feedback, ScanResult, User
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

#--Constants for Model--#
DATA_UPLOAD_FOLDER = 'models/data/user'
DATA_UPLOAD_EXTENSIONS_WHITELIST = { 'png', 'jpg', 'jpeg' }
JSON_FOLDER = 'app/static/json'
SERVER_LOG_PATH = 'log/server.log'

#--global mutable--#
recent_results = {}

#--setup--#
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logFileFormatter = logging.Formatter('%(name)s | %(asctime)s | %(levelname)s: %(message)s', datefmt="%m/%d/%Y %I:%M:%S %p")
logFileHandler = logging.FileHandler(SERVER_LOG_PATH)
logFileHandler.setFormatter(logFileFormatter)
logger.addHandler(logFileHandler)
#-----------------------#

def is_ajax():
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

def render_dashboard_content(template, **kwargs):
    if is_ajax():
        return render_template(template, **kwargs)
    return render_template('dashboard_wrapper.html', content_template=template, **kwargs)

# Home routes
@app.route('/')
@app.route('/home')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('loggedHomePage'))
    return render_template('home-page.html', title='Home')

@app.route('/logged-in/home-page')
@login_required
def loggedHomePage():
    # Add this to ensure it's not using dashboard layout
    return render_template('logged-in/home-page.html', title='home', is_standalone=True)

# About routes (similar modification)

# About routes
@app.route('/about', methods=['GET', 'POST'])
def about():
    if current_user.is_authenticated:
        return redirect(url_for('loggedAbout'))
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

@app.route('/logged-in/about', methods=['GET', 'POST'])
@login_required
def loggedAbout():
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
        return redirect(url_for('loggedAbout') + '#support')
    return render_template('logged-in/about.html', title='About', form=form)

# Auth routes
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
        return redirect(url_for('welcome'))
    return render_template('login-page.html', title='Login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignupForm()
    if form.validate_on_submit():
        try:
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email already in use. Please use a different email.', 'error')
            else:
                user = User(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data
                )
                user.set_pass(form.password.data)
                db.session.add(user)
                db.session.commit()
                return render_template('signup-page.html', title='Signup', form=form, 
                                     success_message='Account created successfully! Redirecting to login page...', 
                                     redirect_url=url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.', 'error')
            app.logger.error(f"Error during signup: {e}")

    return render_template('signup-page.html', title='Signup', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Dashboard routes
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_dashboard_content('dashboard.html', title='Dashboard')

@app.route('/upload', methods=['GET'])
@login_required
def upload():
    form = UploadImage()
    return render_dashboard_content('upload.html', title='Upload', form=form)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_dashboard_content('settings.html', title='Settings')

@app.route('/privacy')
@login_required
def privacy():
    return render_dashboard_content('privacy.html', title='Privacy')

@app.route('/welcome')
@login_required
def welcome():
    return render_dashboard_content('welcome.html', title='welcome')

@app.route('/theme')
@login_required
def theme():
    return render_dashboard_content('theme.html', title='Theme')

# Result routes
@app.route('/result', methods=['GET', 'POST'])
@app.route('/result/<hash>', methods=['GET', 'POST'])
@login_required
def result_page(hash=None):
    img = request.args.get('img')
    result = db.session.scalar(sa.select(ScanResult).where(ScanResult.hash == hash))
    if not result:
        return render_dashboard_content('results-none.html', title='Results None')
    return render_dashboard_content('result.html', result=result, hash=hash, image=img, title='Scan Result')

# User management routes
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def user_edit():
    form = AccountEditForm()
    if form.validate_on_submit():
        updated = False

        if form.delete_account.data:
            db.session.delete(current_user)
            db.session.commit()
            logout_user()
            flash("Your account has been deleted.", "danger")
            return redirect(url_for('index'))

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
            if not check_password_hash(current_user.password_hash, form.old_password.data):
                flash("Incorrect current password.", "danger")
                return redirect(url_for('user_edit'))
            current_user.password_hash = generate_password_hash(form.new_password.data)
            updated = True
        if updated:
            db.session.commit()
            flash("Account updated successfully!", "success")
        else:
            flash("No changes made.", "info")

        return redirect(url_for('user_edit'))
    return render_template('dashboard_wrapper.html', content_template='user-edit.html', title='User Edit', form=form)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    form = PasswordChange()
    return render_template('forgot-password.html', title='Forgot Password', form=form)

# Article routes
@app.route('/feb-article')
def feb_article():
    return render_template('articles/feb-article-list.html')

@app.route('/empty_cab')
def empty_cab():
    return render_template('articles/empty_cab.html')

# News route
@app.route('/news', methods=['GET'])
def get_news():
    if request.method == 'GET':
        json_folder_dir = os.path.join(os.getcwd(), JSON_FOLDER)
        filepath = os.path.join(json_folder_dir, 'news.json')

        time_now = time.time()
        time_created = 0

        dat: dict = {}

        try:
            if not os.path.exists(json_folder_dir):
                os.makedirs(json_folder_dir, exist_ok=True)

            if os.path.exists(filepath):
                time_created = os.path.getctime(filepath)

            if time_created == 0 or time_now - time_created > 2_592_000:
                news_url = f"https://newsapi.org/v2/everything?q=Deepfake&language=en&apiKey={os.getenv('NEWS_SECRET')}"
                logging.info("fetching news data from News API.")
                response = requests.get(news_url)
                dat = response.json()

                with open(filepath, "w", encoding='utf8') as json_file:
                    json.dump(dat, json_file, ensure_ascii=True)
            else:
                with open(filepath, "r") as json_file:
                    dat = json.load(json_file)
        except Exception as e:
            logger.error(f"{e}")

        return dat

# File upload routes
@app.route('/upload', methods=["POST"])
def _file_upload():
    if request.method == 'POST':
        sess = db.session
        if 'file' not in request.files:
            logger.error("File not received.")
            return {"error": "no file found"}, 400

        try:
            file = request.files['file']
            filename = secure_filename(file.filename)
            ext = mse.file_get_extension(filename)
            model_id = request.args.get('model', None) or 'vgg16'

            data_dir = os.path.join(os.getcwd(), DATA_UPLOAD_FOLDER)

            if not os.path.exists(data_dir):
                os.makedirs(data_dir, exist_ok=True)

            if ext.lower() not in DATA_UPLOAD_EXTENSIONS_WHITELIST:
                logger.error(f"File extension is invalid: '{ext}'.")
                return {"error": "file extension blocked"}, 400

            bufpath = os.path.join(data_dir, f"{time.time()}.{ext}")
            file.save(bufpath)

            with open(bufpath, "rb") as bf:
                contents = bf.read()
                hash = hashlib.sha256(contents).hexdigest()
                filepath = os.path.join(data_dir, f"{hash}.{ext}")

            logger.info(f"Received {hash}.")

            if os.path.isfile(filepath):
                os.remove(filepath)

            os.rename(bufpath, filepath)

            static_folder = os.path.join(os.getcwd(), 'app', 'static', 'imgs', 'uploads')
            os.makedirs(static_folder, exist_ok=True)
            static_filepath = os.path.join(static_folder, f"{hash}.{ext}")
            shutil.copy(filepath, static_filepath)

            save_results: bool = True
            result = {}
            if hash in recent_results.keys():
                logger.debug("Hash found locally. Restoring previous result.")
                result = recent_results[hash]

                if result['model'] != model_id:
                    logger.debug("Model mismatch. Sending image to model anyways.")
                    result = mse.prediction(filepath, { 'model_id' : model_id })
                    recent_results[hash] = result
                else:
                    save_results = False
            else:
                queried_result = sess.query(ScanResult).filter(ScanResult.hash == hash).first()

                if queried_result:
                    save_results = False
                    logger.debug("Hash found in database. Restoring previous result.")
                    result = {
                        c.name: getattr(queried_result, c.name) for c in ScanResult.__table__.columns
                        if c.name not in ['status_message', 'status_code', 'status_from']
                    }
                    status = {
                        'message': queried_result.status_message,
                        'code': queried_result.status_code,
                        'from': queried_result.status_from,
                    }
                    result['status'] = status

                    if result['model'] != model_id:
                        logger.debug("Model mismatch. Sending image to model anyways.")
                        result = mse.prediction(filepath, { 'model_id' : model_id })
                        recent_results[hash] = result
                    else:
                       save_results = False
                else:
                    logger.debug("Sending image to model.")
                    result = mse.prediction(filepath, { 'model_id' : model_id })

                recent_results[hash] = result

            logger.debug(f"Validating result: {result}")
        except Exception as e:
            logger.error(f"{e}")
            return {"error": f"Error processing: {str(e)}"}, 500

        finally:
            logger.info("Finished processing. Returning to client.")
            logger.debug(f"hash: {hash}, result: {result}")
            file.close()

            if save_results:
                final_result = ScanResult(
                    hash=hash,
                    time=result['time'],
                    explanation=result['explanation'],
                    model=result['model'],
                    score=result['score'],
                    status_message=result['status']['message'],
                    status_code=result['status']['code'],
                    status_from=result['status']['from']
                )
                sess.add(final_result)
                sess.commit()

        return redirect(url_for('result_page', hash=hash, img=f"{hash}.{ext}"))

@app.route('/upload_ext', methods=["POST"])
def _ext_upload():
    if request.method == 'POST':
        sess = db.session
        if 'file' not in request.files:
            logger.error("File not received.")
            return {"error": "no file found"}, 400

        try:
            file = request.files['file']
            filename = secure_filename(file.filename)
            ext = mse.file_get_extension(filename)
            model_id = request.args.get('model', None) or 'vgg16'

            data_dir = os.path.join(os.getcwd(), DATA_UPLOAD_FOLDER)

            if not os.path.exists(data_dir):
                os.makedirs(data_dir, exist_ok=True)

            if ext.lower() not in DATA_UPLOAD_EXTENSIONS_WHITELIST:
                logger.error(f"File extension is invalid: '{ext}'.")
                return {"error": "file extension blocked"}, 400

            bufpath = os.path.join(data_dir, f"{time.time()}.{ext}")
            file.save(bufpath)

            with open(bufpath, "rb") as bf:
                contents = bf.read()
                hash = hashlib.sha256(contents).hexdigest()
                filepath = os.path.join(data_dir, f"{hash}.{ext}")

            logger.info(f"Received {hash}.")

            if os.path.isfile(filepath):
                os.remove(filepath)

            os.rename(bufpath, filepath)

            static_folder = os.path.join(os.getcwd(), 'app', 'static', 'imgs', 'uploads')
            os.makedirs(static_folder, exist_ok=True)
            static_filepath = os.path.join(static_folder, f"{hash}.{ext}")
            shutil.copy(filepath, static_filepath)

            save_results: bool = True
            result = {}
            if hash in recent_results.keys():
                logger.debug("Hash found locally. Restoring previous result.")
                result = recent_results[hash]

                if result['model'] != model_id:
                    logger.debug("Model mismatch. Sending image to model anyways.")
                    result = mse.prediction(filepath, { 'model_id' : model_id })
                    recent_results[hash] = result
                else:
                    save_results = False
            else:
                queried_result = sess.query(ScanResult).filter(ScanResult.hash == hash).first()

                if queried_result:
                    save_results = False
                    logger.debug("Hash found in database. Restoring previous result.")
                    result = {
                        c.name: getattr(queried_result, c.name) for c in ScanResult.__table__.columns
                        if c.name not in ['status_message', 'status_code', 'status_from']
                    }
                    status = {
                        'message': queried_result.status_message,
                        'code': queried_result.status_code,
                        'from': queried_result.status_from,
                    }
                    result['status'] = status

                    if result['model'] != model_id:
                        logger.debug("Model mismatch. Sending image to model anyways.")
                        result = mse.prediction(filepath, { 'model_id' : model_id })
                        recent_results[hash] = result
                    else:
                       save_results = False
                else:
                    logger.debug("Sending image to model.")
                    result = mse.prediction(filepath, { 'model_id' : model_id })

                recent_results[hash] = result

            logger.debug(f"Validating result: {result}")
        except Exception as e:
            logger.error(f"{e}")
            return {"error": f"Error processing: {str(e)}"}, 500

        finally:
            logger.info("Finished processing. Returning to client.")
            logger.debug(f"hash: {hash}, result: {result}")
            file.close()

            ext_response = {
                "hash": hash,
                "explanation": result['explanation'],
                "score": result['score'],
            }

        return json.dumps(ext_response)