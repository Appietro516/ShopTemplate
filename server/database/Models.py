from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def initializeDB():
    db.create_all()
    db.session.commit()