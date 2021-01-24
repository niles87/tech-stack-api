import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class Config(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(os.path.abspath(os.path.dirname(__file__)),
                     os.getenv("DATABASE_URL"))


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv("PRODUCTION_SECRET")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    SECRET_KEY = os.getenv("DEV_SECRET")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
