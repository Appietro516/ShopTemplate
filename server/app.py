from flask import Flask
from flask_cors import CORS
import settings
import sys
from database.Models import db
import database.User as Users

DEBUG = True
app = Flask(__name__, static_folder='static')

# Import routes defined by app
import views.Admin
import views.Checkout
import views.Shop

# configure
app.config.from_object(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = settings.DB_URL
db.init_app(app)

# First time setup
if len(sys.argv) > 1 and sys.argv[1] == 'setup':
    with app.app_context():
        db.create_all()
    Users.signup(settings.EMAIL, settings.PASSWORD)

# cors
CORS(app, resources={r'/*': {'origins': '*'}})

# start server
if __name__ == '__main__':
    app.run(host='0.0.0.0')