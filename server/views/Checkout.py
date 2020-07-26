from __main__ import app
from flask import Flask, jsonify, request
from database.Models import db
import database.Products as Products
import database.User as Users
import database.Customers as Customers
import database.Orders as Orders
import database.OrderDetails as OrderDetails
import stripe
import settings


#***************************************************
#              CHECKOUT ROUTES                     *
#***************************************************

@app.route('/customer', methods=['POST'])
def get_details():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if Customers.is_authenticated(email, password):

        return jsonify({
            'status': 'success',
            'data': Customers.get_customer_info(email, password)
        }), 200

    return jsonify({
        'status': 'failure',
        'message': 'invalid credentials'
    }), 400


@app.route('/purchase', methods=['POST'])
def purchase_products():
    data = request.get_json()
    returning_customer = data.get('returningCustomer')
    email = data.get('email')
    products_selected = data.get('items')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    address = data.get('address')
    appartment = data.get('appartment')
    city = data.get('city')
    state = data.get('state')
    country = data.get('country')
    zip_code = data.get('zipCode')
    phone_number = data.get('phoneNumber')

    # Validate products selected
    if products_selected is None:
        return jsonify({
            'status': 'failure',
            'message': 'no products found'
        }), 400
    else:
        for item in products_selected:
            if not Products.get(item['id']):
                return jsonify({
                    'status': 'failure',
                    'message': 'one or more invalid products'
                }), 400

    customer_id = None
    if returning_customer:
        if email is None or password is None:
            return jsonify({
                'status': 'failure',
                'message': 'Missing email or password'
            }), 400

        customer_id = Customers.get_customer_id(email, password)
    else:
        if (first_name is None or last_name is None or
            email is None or address is None or city is None or
            country is None or zip_code is None or phone_number is None):
            return jsonify({
                'status': 'failure',
                'message': 'Missing important information'
            }), 400

        customer_id = Customers.add(first_name, last_name, email, password, address, 
                appartment, city, country, state, zip_code, phone_number)

    product_orders = []
    for item in products_selected:
        if item['quantity'] > 0:
            product = Products.get(item['id'])
            order_id = OrderDetails.new(product.id, item['quantity'], product.price)
            product_orders.append(order_id)

    if customer_id is not None and product_orders is not None:
        Orders.new(customer_id, product_orders)
    else:
        return jsonify({ 'status': 'failure' }), 500
    
    return jsonify({ 'status': 'success' }), 200


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