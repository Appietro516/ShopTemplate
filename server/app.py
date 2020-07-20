import os
import stripe
from flask import Flask, jsonify, request
from flask_cors import CORS
import settings
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__, static_folder='static')
app.config.from_object(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = settings.DB_URL

# --------------------- DATABASE TABLES --------------------- #
'''
    Product class holds all products.
'''
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    price = db.Column(db.Float, unique=False)
    description = db.Column(db.String(255), unique=False)
    image = db.Column(db.String(100), unique=False)

    def __init__(self, name, price, description, image):
        self.name = name
        self.price = price
        self.description = description
        self.image = image
    
    def __repr__(self):
        return f'<id {self.id}>'

'''
    User class is used to hold admin credentials for modifying shop.
'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15))
    password = db.Column(db.String(15), unique=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<username {self.username}>'


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# --------------------- FOOD SHOP ROUTES --------------------- #


@app.route('/products/new', methods=['POST'])
def upload_product():
    name = request.json['name']
    price = request.json['price']
    description = request.json.get('description', None)
    image = request.json.get('image', None)
    
    product = Product(name, price, description, image)
    db.session.add(product)
    db.session.commit()
    response_object = {
        'status': 'success',
        'message': 'item inserted into database'
    }
    return jsonify(response_object), 200


@app.route('/products/<int:id>/update', methods=['PUT', 'DELETE'])
def update_product(id):
    if request.method == 'PUT':
        name = request.json.get('name', None)
        price = request.json.get('price', None)
        description = request.json.get('description', None)
        image = request.json.get('image', None)
        
        if not name and not price and not description and not image:
            response_object = {
                'status': 'failure',
                'message': 'Empty request'
            }
            return jsonify(response_object), 400

        product = Product.query.get(id)

        if not product:
            response_object = {
                'status': 'failure',
                'message': 'invalid product id'
            }
            return jsonify(response_object), 400

        if name:
            product.name = name
        if price:
            product.price = price
        if description:
            product.description = description
        if image:
            product.image = image

        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'item was updated in table'
        }
        return jsonify(response_object), 200
    if request.method == 'DELETE':
        try:
            if not Product.query.get(id):
                raise SQLAlchemyError

            Product.query.filter_by(id=id).delete()
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'item was deleted from table'
            }
            return jsonify(response_object), 200
        except SQLAlchemyError:
            response_object = {
            'status': 'failure',
            'message': 'Item not in table'
        }
        return jsonify(response_object), 400


@app.route('/products', methods=['GET'])
def get_products():
    try:
        response_object = {
            'status': 'success',
            'products': []
        }

        products = Product.query.all()

        if not products:
            raise SQLAlchemyError

        for item in products:
            response_object['products'].append({
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'description': item.description,
                'image': item.image
            })

        return jsonify(response_object), 200
    except SQLAlchemyError:
        response_object = {
            'status': 'failure',
            'message': 'Empty table or invalid connection'
        }
        return jsonify(response_object), 500
    except:
        response_object = {
            'status': 'failure',
            'message': 'server error encountered'
        }
        return jsonify(response_object), 500


@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    try:
        product = Product.query.get(id)
        if not product:
            raise SQLAlchemyError

        response_object = {
            'status': 'success',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'description': product.description,
                'image': product.image
            }
        }
        return jsonify(response_object), 200
             
    except SQLAlchemyError:
        response_object = {
            'status': 'failure',
            'message': 'Invalid product id'
        }
        return jsonify(response_object), 400

    except:
        response_object = {
            'status': 'failure',
            'message': 'Server issue encoutered'
        }
        return jsonify(response_object), 500


# --------------------- CHECKOUT ROUTES --------------------- #


@app.route('/charge', methods=['POST'])
def create_charge():
    post_data = request.get_json()
    amount = round(float(post_data.get('product')['price']) * 100)
    stripe.api_key = settings.STRIPE_KEY
    
    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency='usd',
            card=post_data.get('token'),
            description=post_data.get('product')['name']
        )
        response_object = {
            'status': 'success',
            'charge': charge
        }
        return jsonify(response_object), 200
    except stripe.error.CardError:
        response_object = {
            'status': 'failure',
            'message': 'invalid card details'
        }
        return jsonify(response_object), 400
    except:
        response_object = {
            'status': 'failure',
            'message': 'server issue incountered'
        }
        return jsonify(response_object), 500


@app.route('/charge/<charge_id>')
def get_charge(charge_id):
    stripe.api_key = settings.STRIPE_KEY
    response_object = {
        'status': 'success',
        'charge': stripe.Charge.retrieve(charge_id)
    }
    return jsonify(response_object), 200


# --------------------- START SERVER --------------------- #

if __name__ == '__main__':
    #db.create_all()
    app.run()