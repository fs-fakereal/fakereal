
import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

config = configparser.ConfigParser()
config.read('config.ini')

Base = declarative_base()


def get_connection():
    return create_engine(url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
        config['Database']['user'], config['Database']['pass'], config['Database']['host'], config['Database']['port'], config['Database']['db']
    ))
