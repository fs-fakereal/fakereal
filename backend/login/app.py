import os

import psycopg2

from flask import Flask

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(...)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()

