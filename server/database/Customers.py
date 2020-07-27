from database.Models import db  
import settings
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

'''
    Password is optional, except users with no password are unable to checkout
    as a returning user and unable to access their account.
'''
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), unique=False)
    last_name = db.Column(db.String(50), unique=False)
    email = db.Column(db.String(120), unique=False)
    address = db.Column(db.String(120), unique=False)
    appartment = db.Column(db.String(120), unique=False)
    city = db.Column(db.String(120), unique=False)
    country = db.Column(db.String(120), unique=False)
    state = db.Column(db.String(120), unique=False)
    zip_code = db.Column(db.String(10), unique=False)
    phone_number = db.Column(db.String(15), unique=False)
    password = db.Column(db.String(255), unique=False)
    datetimecreated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, first, last, email, password, address, appartment, city, country, state, zip, phone):
        self.first_name = first
        self.last_name = last
        self.email = email.lower()
        if password:
            self.password = generate_password_hash(password, method='sha256')
        else:
            self.password = 'NONE'
        self.address = address
        self.appartment = appartment
        self.city = city
        self.state = state
        self.country = country
        self.zip_code = zip
        self.phone_number = phone

    @classmethod
    def authenticate(cls, email, password):
        if not email or not password:
            return None
        customer = cls.query.filter_by(email=email).first()
        if not customer or customer.password == 'NONE' or not check_password_hash(customer.password, password):
            return None
        return customer
    
    def __repr__(self):
        return f'<id {self.id}>'


def add(first, last, email, password, address, appartment, city, country, state, zip, phone):
    customer = Customer(first, last, email, password, address, appartment, city, country, state, zip, phone)
    db.session.add(customer)
    db.session.commit()

    return customer.id

def is_authenticated(email, password):
    return Customer.authenticate(email, password) is not None

def get_customer_info(email, password):
    if is_authenticated(email, password):
        customer = Customer.query.filter_by(email=email.lower()).first()
        data = {
            'address': customer.address,
            'appartment': customer.appartment,
            'city': customer.city,
            'state': customer.state,
            'country': customer.country,
            'zipCode': customer.zip_code,
            'phoneNumber': customer.phone_number
        }
        return data
    return 'NO CUSTOMER DATA'

def get_shipment_info(id):
    customer = Customer.query.get(id)
    data = {
        'firstName': customer.first_name,
        'lastName': customer.last_name,
        'email': customer.email,
        'address': customer.address,
        'appartment': customer.appartment,
        'city': customer.city,
        'state': customer.state,
        'country': customer.country,
        'zipCode': customer.zip_code,
        'phoneNumber': customer.phone_number
    }
    return data

def get_customer_id(email, password):
    if is_authenticated(email, password):
        customer = Customer.query.filter_by(email=email.lower()).first()
        return customer.id