import os
import stripe
from flask import Flask, jsonify, request
from flask_cors import CORS
import settings
from datetime import datetime, timedelta
from functools import wraps
import jwt
import sys
import database.Models as Model
import database.Products as Products
import database.User as Users

DEBUG = True
app = Flask(__name__, static_folder='static')
app.config.from_object(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = settings.DB_URL
Model.db.init_app(app)
CORS(app, resources={r'/*': {'origins': '*'}})

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
            if not Users.isValidUser(data['sub']):
                raise RuntimeError('User not found')
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401
    
    return _verify

#***************************************************
#              AUTHENTICATE USER                   *
#***************************************************

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Users.authenticateUser(**data)
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

#***************************************************
#                PRODUCT ROUTES                    *
#***************************************************

@app.route('/ping', methods=['POST'])
@token_required
def ping():
    return jsonify({'message': 'pong'})

@app.route('/products/new', methods=['POST'])
@token_required
def upload_product():
    name = request.json['name']
    price = request.json['price']
    description = request.json.get('description', None)
    image = request.json.get('image', None)
    
    Products.addProduct(name, price, description, image)

    response_object = {
        'status': 'success',
        'message': 'item inserted into database'
    }
    return jsonify(response_object), 201


@app.route('/products/<int:id>/update', methods=['PUT', 'DELETE'])
@token_required
def update_product(id):
    if request.method == 'PUT':
        name = request.json.get('name', None)
        price = request.json.get('price', None)
        description = request.json.get('description', None)
        image = request.json.get('image', None)
        
        if (not name and not price
            and not description and not image):
            response_object = {
                'status': 'failure',
                'message': 'Empty request'
            }
            return jsonify(response_object), 400

        if not Products.isValidProduct(id):
            response_object = {
                'status': 'failure',
                'message': 'invalid product id'
            }
            return jsonify(response_object), 400

        Products.updateProduct(id, name, price, description, image)

        response_object = {
            'status': 'success',
            'message': 'item was updated in table'
        }
        return jsonify(response_object), 200
    if request.method == 'DELETE':

        if not Products.isValidProduct(id):
            response_object = {
                'status': 'failure',
                'message': 'Item not in table'
            }
            return jsonify(response_object), 400

        Products.deleteProduct(id)

        response_object = {
            'status': 'success',
            'message': 'item was deleted from table'
        }
        return jsonify(response_object), 200


@app.route('/products', methods=['GET'])
def get_products():
    try:
        response_object = {
            'status': 'success',
            'products': []
        }

        products = Products.getAll()

        if not products:
            response_object = {
                'status': 'success',
                'message': 'No content available'
            }
            return jsonify(response_object), 204

        for item in products:
            response_object['products'].append({
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'description': item.description,
                'image': item.image
            })

        return jsonify(response_object), 200
    except:
        response_object = {
            'status': 'failure',
            'message': 'server error encountered'
        }
        return jsonify(response_object), 500


@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    try:
        product = Products.get(id)
        if not product:
            response_object = {
                'status': 'failure',
                'message': 'Invalid product id'
            }
            return jsonify(response_object), 400

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

    # First time setup
    if len(sys.argv) > 1 and sys.argv[1] == 'setup':
        Model.initializeDB()
        Users.signup(settings.EMAIL, settings.PASSWORD)

    app.run()