from database.Models import db  
import settings
import datetime

class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, unique=False)
    quantity = db.Column(db.Integer, unique=False)
    item_cost = db.Column(db.Float, unique=False)
    datetimecreated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, product, quantity, cost):
        self.product_id = product
        self.quantity = quantity
        self.item_cost = cost
    
    def __repr__(self):
        return f'<id {self.id}>'


def new(product, quantity, cost):
    order_detail = OrderDetail(product, quantity, cost)
    db.session.add(order_detail)
    db.session.commit()

    return order_detail.id

def get(id):
    return OrderDetail.query.get(id)