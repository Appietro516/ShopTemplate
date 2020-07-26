from __main__ import app
from flask import Flask, jsonify, request
from database.Models import db
import database.Products as Products
import database.User as Users
import database.Customers as Customers
import database.Orders as Orders
import database.OrderDetails as OrderDetails
from datetime import datetime, timedelta
import jwt
import settings
from functools import wraps

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
        'token': token.decode('UTF-8'),
        }), 200

#***************************************************
#                ADMIN ROUTES                    *
#***************************************************
  
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
