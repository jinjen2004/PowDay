# models/ski_resort.py
from . import db

class SkiResort(db.Model):
    __tablename__ = "ski_resorts"
    id = db.Column(db.Integer, primary_key=True)
    resort_name = db.Column(db.String(100))
    state = db.Column(db.String(2))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    lift_ticket_price_weekday_usd = db.Column(db.Float)
    lift_ticket_price_weekend_usd = db.Column(db.Float)
    difficulty_beginner_pct = db.Column(db.Integer)
    difficulty_intermediate_pct = db.Column(db.Integer)
    difficulty_advanced_pct = db.Column(db.Integer)
    busiest_days = db.Column(db.String(255))
    annual_snowfall_inches = db.Column(db.Integer)
    skiable_acres = db.Column(db.Integer)
    vertical_drop_ft = db.Column(db.Integer)
    pass_type = db.Column(db.String(50))
    allow_snowboard = db.Column(db.Boolean)
