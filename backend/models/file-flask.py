# NOTE(liam): flask impl of file.py

import sys
# load files in py dir
sys.path.insert(1, './py')

import hashlib
import json

import model
from db import Base, get_connection

from flask import Flask, request
from flask_cors import CORS, cross_origin

from PIL import Image
from sqlalchemy.orm import sessionmaker

#--Constants--#
DEBUG = True
recent_results = {}
#-------------#


app = Flask(__name__)
cors = CORS(app, resources={
    # NOTE(liam): change this when serving live.
    "/": { "origins": "*" },
    "/upload": { "origins": "*" },
})
app.config['CORS_HEADERS'] = 'Content-Type'

db_engine = get_connection()
Base.metadata.create_all(bind=db_engine)
Session = sessionmaker(bind=db_engine)
s = Session()

@app.route('/')
def hello():
    return "<h1>Conn Established!</h1>"

@app.route('/upload', methods=["POST"])
def _file_upload():
    if request.method == 'POST':
        try:
            file = request.files['file']
            if not file:
                raise Exception()

            filename = file.filename

            contents = file.read()
            hash = hashlib.sha256(contents).hexdigest()

            if hash in recent_results.keys():
                if DEBUG:
                    print("INFO: Hash found. Restoring previous result.")
                result = recent_results[hash]
            else:
                if DEBUG:
                    print("INFO: Sending image to model.")

                result = model.parse_check(model.check_media(filename))
                recent_results[hash] = result

            model.push_results(s, result, hash)

        except Exception as e:
            print(f"ERROR: {e}")

        finally:
            if DEBUG:
                print("INFO: Finished processing. Returning to client.")
            file.close()

        return { "hash": hash, "result": result }

if __name__ == "__main__":
    app.run()
