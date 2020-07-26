from database.Models import db
import settings

'''
    Represents a single product
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

  
def addProduct(name, price, description, image):
    product = Product(name, price, description, image)
    db.session.add(product)
    db.session.commit()


def updateProduct(id, name, price, description, image):
    product = Product.query.get(id)
    if product:
        if name:
            product.name = name
        if price:
            product.price = price
        if description:
            product.description = description
        if image:
            product.image = image

        db.session.commit()


def deleteProduct(id):
    if Product.query.get(id):
        Product.query.filter_by(id=id).delete()
        db.session.commit()


def getAll():
    return Product.query.all()


def get(id):
    return Product.query.get(id)


def isValidProduct(id):
    product = Product.query.get(id)
    return product is not None