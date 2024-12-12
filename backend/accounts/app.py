import os

import psycopg2
from dotenv import dotenv_values, load_dotenv
from flask import Flask, request
from flask_cors import CORS, cross_origin

from middleware import middleware

load_dotenv()

#os.getenv("MONGO_URI")

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = "Content-Type"

app.wsgi_app = middleware(app.wsgi_app)

@app.route('/')
@cross_origin()
def index():
    user = request.environ['user']
    return f"hi {user['name']}"

def get_db_connection():
    conn = psycopg2.connect(os.getenv("MONGO_URI"))
    if conn:
        return "success."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT")), debug=True)

