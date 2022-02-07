import json

from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from functions import get_data, convert_user_to_dict, convert_order_to_dict, convert_offer_to_dict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String, unique=True)
    role = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    orders = db.relationship('Order', foreign_keys=[order_id])
    executors = db.relationship('User', foreign_keys=[executor_id])


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    customers = db.relationship('User', foreign_keys=[customer_id])
    executors = db.relationship('User', foreign_keys=[executor_id])


db.create_all()

users_data = get_data('Users_data.json')
users_list = []
for row in users_data:
    users_list.append(User(id=row['id'],
                           first_name=row['first_name'],
                           last_name=row['last_name'],
                           age=row['age'],
                           email=row['email'],
                           role=row['role'],
                           phone=row['phone']))

db.session.add_all(users_list)
db.session.commit()

offers_data = get_data('Offers_data.json')
offers_list = []
for row in offers_data:
    offers_list.append(Offer(id=row['id'],
                             order_id=row['order_id'],
                             executor_id=row['executor_id']))

db.session.add_all(offers_list)
db.session.commit()

orders_data = get_data('Orders_data.json')
orders_list = []
for row in orders_data:
    orders_list.append(Order(id=row['id'],
                             name=row['name'],
                             description=row['description'],
                             start_date=row['start_date'],
                             end_date=row['end_date'],
                             address=row['address'],
                             price=row['price'],
                             customer_id=row['customer_id'],
                             executor_id=row['executor_id']))

db.session.add_all(orders_list)
db.session.commit()


@app.route('/users', methods=["GET", "POST"])
def all_users():
    if request.method == "GET":
        users_dict_list = []
        users = User.query.all()
        for user in users:
            users_dict_list.append(convert_user_to_dict(user))
        return jsonify(users_dict_list), 200, {'Content-Type': 'application/json; charset=utf-8'}

    elif request.method == "POST":
        user_data = json.loads(request.data)
        new_user = User(id=user_data['id'],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        age=user_data['age'],
                        email=user_data['email'],
                        role=user_data['role'],
                        phone=user_data['phone'])
        db.session.add(new_user)
        db.session.commit()
        return "", 201


@app.route('/users/<int:id_>', methods=["GET", "PUT", "DELETE"])
def user_by_id(id_: int):
    if request.method == "GET":
        user = User.query.get(id_)
        if user:
            return jsonify(convert_user_to_dict(user)), 200, {'Content-Type': 'application/json; charset=utf-8'}
        abort(400, "Пользователь не найден")

    elif request.method == 'DELETE':
        user = User.query.get(id_)
        db.session.delete(user)
        db.session.commit()
        return "", 200

    elif request.method == "PUT":
        user_data = request.json
        new_user = User.query.get(id_)
        if new_user:
            new_user.first_name = user_data['first_name']
            new_user.last_name = user_data['last_name']
            new_user.age = user_data['age']
            new_user.email = user_data['email']
            new_user.ole = user_data['role']
            new_user.phone = user_data['phone']

            db.session.add(new_user)
            db.session.commit()
            return "", 200


@app.route('/orders', methods=["GET", "POST"])
def all_orders():
    if request.method == "GET":
        orders_dict_list = []
        orders = Order.query.all()
        for order in orders:
            orders_dict_list.append(convert_order_to_dict(order))
        return jsonify(orders_dict_list), 200, {'Content-Type': 'application/json; charset=utf-8'}

    elif request.method == "POST":
        order_data = request.json
        new_order = Order(id=order_data['id'],
                          name=order_data['name'],
                          description=order_data['description'],
                          start_date=order_data['start_date'],
                          end_date=order_data['end_date'],
                          address=order_data['address'],
                          price=order_data['price'],
                          customer_id=order_data['customer_id'],
                          executor_id=order_data['executor_id'])

        db.session.add(new_order)
        db.session.commit()
        return "", 201


@app.route('/orders/<int:id_>', methods=["GET", "PUT", "DELETE"])
def order_by_id(id_: int):
    if request.method == "GET":
        order = Order.query.get(id_)
        if order:
            return jsonify(convert_order_to_dict(order)), 200, {'Content-Type': 'application/json; charset=utf-8'}
        abort(400, "Заказ не найден")

    elif request.method == 'DELETE':
        order = Order.query.get(id_)
        db.session.delete(order)
        db.session.commit()
        return "", 200

    elif request.method == "PUT":
        order_data = request.json
        new_order = Order.query.get(id_)
        if new_order:
            new_order.name = order_data['name']
            new_order.description = order_data['description']
            new_order.start_date = order_data['start_date']
            new_order.end_date = order_data['end_date']
            new_order.address = order_data['address']
            new_order.price = order_data['price']
            new_order.customer_id = order_data['customer_id']
            new_order.executor_id = order_data['executor_id']

            db.session.add(new_order)
            db.session.commit()
            return "", 200


@app.route('/offers', methods=["GET", "POST"])
def all_offers():
    if request.method == "GET":
        offers_dict_list = []
        offers = Offer.query.all()
        for offer in offers:
            offers_dict_list.append(convert_offer_to_dict(offer))
        return jsonify(offers_dict_list), 200, {'Content-Type': 'application/json; charset=utf-8'}

    elif request.method == "POST":
        offer_data = request.json
        new_offer = Offer(id=offer_data['id'],
                          order_id=offer_data['order_id'],
                          executor_id=offer_data['executor_id'])
        db.session.add(new_offer)
        db.session.commit()
        return "", 201


@app.route('/offers/<int:id_>', methods=["GET", "PUT", "DELETE"])
def offer_by_id(id_: int):
    if request.method == "GET":
        offer = Offer.query.get(id_)
        if offer:
            return jsonify(convert_offer_to_dict(offer)), 200, {'Content-Type': 'application/json; charset=utf-8'}
        abort(400, "Предложение не найдено")

    elif request.method == 'DELETE':
        offer = Offer.query.get(id_)
        db.session.delete(offer)
        db.session.commit()
        return "", 200

    elif request.method == "PUT":
        offer_data = request.json
        new_offer = Offer.query.get(id_)
        if new_offer:
            new_offer.order_id = offer_data['order_id']
            new_offer.executor_id = offer_data['executor_id']

            db.session.add(new_offer)
            db.session.commit()
            return "", 200


if __name__ == '__main__':
    app.run(debug=True)
