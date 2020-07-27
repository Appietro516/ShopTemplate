from __main__ import app
from flask import Flask, jsonify, request
from database.Models import db
import database.Products as Products
import database.User as Users
import database.Customers as Customers
import database.Orders as Orders
import database.OrderDetails as OrderDetails
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Limit amount of calls made by a user
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/products', methods=['GET'])
@limiter.exempt
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
@limiter.exempt
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
