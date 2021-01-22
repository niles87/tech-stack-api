from enum import unique
from flask_sqlalchemy import SQLAlchemy
import click
from flask import current_app, g
from flask.cli import cli, with_appcontext


db = SQLAlchemy(current_app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return '<User %r' % self.name


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    available_stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __repr__(self) -> str:
        return '<Stock %r' % self.name


def close_db():
    pass


def init_db():
    db.create_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the db")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
