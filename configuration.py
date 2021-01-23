import os


class Config(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(os.path.abspath(os.path.dirname(__file__)),
                     os.environ.get("DATABASE_URL"))


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get("PRODUCTION_SECRET")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    SECRET_KEY = os.environ.get("DEV_SECRET")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
