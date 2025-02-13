# NOTE(liam): flask impl of file.py

import sys
# load files in py dir
sys.path.insert(1, './py')

import hashlib
import json
import os
import time

import model
from db import Base, get_connection

from flask import flash, flash, Flask, request
from flask_cors import CORS, cross_origin

from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename

#--Constants--#
DEBUG = True
recent_results = {}
UPLOAD_FOLDER = './data'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg' }
#-------------#


app = Flask(__name__)
cors = CORS(app, resources={
    # NOTE(liam): change this when serving live.
    "/": { "origins": "*" },
    "/upload": { "origins": "*" },
})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db_engine = get_connection()
Base.metadata.create_all(bind=db_engine)
Session = sessionmaker(bind=db_engine)
s = Session()

def file_get_extension(filename):
    return filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''

@app.route('/')
def hello():
    return "<h1>Conn Established!</h1>"

@app.route('/upload', methods=["POST"])
def _file_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return {"error": "no file found"}, 400

        try:
            # NOTE(liam): file processing section
            file = request.files['file']
            filename = secure_filename(file.filename)
            ext = file_get_extension(filename)

            if ext not in ALLOWED_EXTENSIONS:
                return {"error": "file extension blocked"}, 400

            # NOTE(liam): saves file temporarily
            bufpath = os.path.join(app.config['UPLOAD_FOLDER'], f"{time.time()}.{ext}")
            file.save(bufpath)

            # NOTE(liam): file.read() and file.save() is a blocking process,
            # so basically I can't run either one after the other.
            # Idk how else to fix this than what I did here.
            with open(bufpath, "rb") as bf:
                contents = bf.read()
                hash = hashlib.sha256(contents).hexdigest()
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{hash}.{ext}")


            # TODO(liam): this is definitely not efficient,
            # but it works, so good enough for now.
            if not (os.path.isfile(filepath)):
                os.rename(bufpath, filepath)
            else:
                os.remove(bufpath)

            result = ""
            if hash in recent_results.keys():
                if DEBUG:
                    print("INFO: Hash found. Restoring previous result.")
                result = recent_results[hash]
            else:
                if DEBUG:
                    print("INFO: Sending image to model.")

                result = model.parse_check(model.check_media(filepath))
                recent_results[hash] = result

            #model.push_results(s, result, hash)

        except Exception as e:
            print(f"ERROR: {e}")
            return {"error": f"Error processing file: {str(e)}"}, 500

        finally:
            if DEBUG:
                print("INFO: Finished processing. Returning to client.")
            file.close()

        return { "hash": hash, "result": result }

if __name__ == "__main__":
    app.run()
