
import os

from dotenv import dotenv_values, load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


Base = declarative_base()

load_dotenv()

def get_connection():
    return create_engine(url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
        os.getenv('USER'), os.getenv('PASS'), os.getenv('HOST'), os.getenv('PORT'), os.getenv('DB')
    ))
