from database.Models import db  
import settings
import datetime



class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, unique=False)
    purchased_items = db.Column(db.String(250), unique=False)
    datetimecreated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.Integer, unique=False)
    tracking_website = db.Column(db.String(120), unique=False)

    def __init__(self, customer, items):
        self.customer_id = customer
        self.purchased_items = ';'.join(str(x) for x in items)
        self.status = 0

    @property
    def items(self):
        return [int(x) for x in self._purchased_items.split(';')]

    def status_string(self):
        status_dict = {
            0: 'in progress',
            1: 'shipping',
            2: 'delivered'
        }
        return status_dict[self.status]
    
    def __repr__(self):
        return f'<id {self.id}>'

def new(customer, items):
    order = Order(customer, items)
    db.session.add(order)
    db.session.commit()
    return order.id