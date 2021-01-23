from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from .extentions import db, ma


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

    def __init__(self, name, price, qty, description):
        self.name = name
        self.price = price
        self.available_stock = qty
        self.description = description


class StockSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price', 'available_stock', 'description')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')


stock_schema = StockSchema(many=True, strict=True)
user_schema = UserSchema(strict=True)
