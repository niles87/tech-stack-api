import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('configuration.DevelopmentConfig')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .extentions import db, ma
    db.init_app(app)
    ma.init_app(app)

    @app.route("/hello")
    def hello():
        return 'Hello world'

    return app
