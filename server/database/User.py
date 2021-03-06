from database.Models import db
from werkzeug.security import generate_password_hash, check_password_hash
import settings  

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

def signup(email, password):
    user = User(email, password)
    db.session.add(user)
    db.session.commit()

def authenticateUser(**kwargs):
    return User.authenticate(**kwargs)


def isValidUser(email):
    return User.query.filter_by(email=email).first() is not None