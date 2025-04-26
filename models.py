from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SkiResort(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    difficulty = db.Column(db.String(50))
    price = db.Column(db.Float)
    busiest_days = db.Column(db.String(100))
    # Add other fields as needed
