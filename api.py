import os
from flask import Flask, request
from flask.json import jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config.from_object('configuration.DevelopmentConfig')

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


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


stock_schema = StockSchema(many=True)
item_schema = StockSchema()


@app.route('/stock', methods=['GET', 'POST'])
def stock():
    if request.method == 'POST':
        name = request.json['name']
        price = request.json['price']
        qty = request.json['qty']
        description = request.json['description']

        new_item = Stock(name, price, qty, description)

        db.session.add(new_item)
        db.session.commit()

        return item_schema.jsonify(new_item)
    elif request.method == 'GET':
        all_stock = Stock.query.all()
        result = stock_schema.dump(all_stock)
        return jsonify(result)


@app.route('/auth/register', methods=['POST'])
def register():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    new_customer = Customer(name, email, generate_password_hash(password))

    db.session.add(new_customer)
    db.session.commit()

    return {
        "id": new_customer.id,
        "name": new_customer.name,
        "email": new_customer.email
    }


@app.route('/auth/login', methods=['POST'])
def login():
    customer = Customer.query.filter_by(email=request.json['email']).first()

    password = request.json['password']

    if customer is None:
        return {}, 401
    elif not check_password_hash(customer.password, password):
        return {}, 401
    else:
        return {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email
        }


if __name__ == '__main__':
    app.run()
