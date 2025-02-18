import os
basedir = os.path.abspath(os.path.dirname(__file__))

#this is a config file for variables/settings used by flask
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] <- use during production
    #use file with environment variables upon production
    USER = os.environ['USER']
    PASSWORD = os.environ['PASSWORD']
    HOST = os.environ['HOST']
    PORT = os.environ['PORT']
    DBNAME = os.environ['DBNAME']
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True