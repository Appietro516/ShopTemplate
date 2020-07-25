import os
import stripe
from flask import Flask, jsonify, request
from flask_cors import CORS
import settings
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import sys 

DEBUG = True
app = Flask(__name__, static_folder='static')
app.config.from_object(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = settings.DB_URL
db = SQLAlchemy(app)
CORS(app, resources={r'/*': {'origins': '*'}})

#***************************************************
#              DATABASE TABLES                     *
#***************************************************
'''
    Product class holds all products.
'''
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    price = db.Column(db.Float, unique=False)
    description = db.Column(db.String(255), unique=False)
    image = db.Column(db.String(100), unique=False)
    quantity = db.Column(db.Integer, unique=False)

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
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(id=self.id, email=self.email)

#***************************************************
#              AUTHENTICATION                      *
#***************************************************

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.json['authorization'].split()

        invalid_msg = {
            'message': 'Invalid credentials. login required',
            'authenticated': False
        }

        expired_msg = {
            'message': 'Expired session. Reauthentication required',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401
        try:
            token = auth_headers[1]
            data = jwt.decode(token, settings.SECRET_KEY)
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')

            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401
    
    return _verify

#***************************************************
#                    ROUTES                        *
#***************************************************

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.authenticate(**data)
    if not user:
        return jsonify({
            'status': 'failure',
            'message': 'Invalid credentials'
        }), 401

    token = jwt.encode({
        'sub': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        settings.SECRET_KEY)
    return jsonify({
        'status': 'success',
        'token': token.decode('UTF-8')
        }), 200


@app.route('/products/new', methods=['POST'])
@token_required
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
    return jsonify(response_object), 201


@app.route('/products/<int:id>/update', methods=['PUT', 'DELETE'])
@token_required
def update_product(id):
    if request.method == 'PUT':
        #id = request.json.get('id', None)
        name = request.json.get('name', None)
        price = request.json.get('price', None)
        description = request.json.get('description', None)
        image = request.json.get('image', None)
        
        if (not id and not name and not price 
            and not description and not image):
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


#***************************************************
#              CHECKOUT ROUTES                     *
#***************************************************


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


@app.route('/charge/<charge_id>', methods=['GET'])
def get_charge(charge_id):
    stripe.api_key = settings.STRIPE_KEY
    response_object = {
        'status': 'success',
        'charge': stripe.Charge.retrieve(charge_id)
    }
    return jsonify(response_object), 200

#***************************************************
#                 START SERVER                     *
#***************************************************

if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == 'setup':
        # Setup database with single user
        db.create_all()
        user = User(settings.USER_NAME, settings.PASSWORD)
        db.session.add(user)
        db.session.commit()

    app.run()