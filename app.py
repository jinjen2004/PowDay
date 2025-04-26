import pandas as pd
import os, time, requests, functools, time 
from typing import Dict, Any, List 
from models import db
from models.ski_resort import SkiResort
from utils.geo import geocode, haversine_mi
from utils.weather import current, hourly, daily, ski_summary
from geopy.exc import GeocoderServiceError # for error on distance search


from flask import Flask, render_template, request #Q0: What happens if you remove render_template from this line?

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ski_resorts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context(): # Database
    db.create_all()

# Our weather API
BASE = "https://api.openweathermap.org/data"
API_KEY = "6a8dc08d5123e7c104b59aa3b4c138d1" # <- terrible practice o well

@app.route("/")
def home():
    return render_template('home.html', user="Test Test")

@app.route("/explore")
def explore():
    resorts = [
        ["Vail", "this is a cool resort"],
        ["Breckenridge", "really hard"],
        ["Park City Mountain", "awesome awesome awesome"]
    ]
    return render_template('explore.html', collection=resorts)

    # The images are referenced by the resort name and are in the static/img folder. Works for now but might not be the best system, storing the image path may be better.

@app.route("/search", methods=["GET"])
def search():
    if not request.args:
        return render_template("search.html")

    q = SkiResort.query

    # Pass type filter
    pass_type = request.args.get("pass")
    if pass_type and pass_type != "Any":
        q = q.filter(SkiResort.pass_type == pass_type)

    # Price filter
    price = request.args.get("price")
    if price == "$":
        q = q.filter(SkiResort.lift_ticket_price_weekend_usd < 150)
    elif price == "$$":
        q = q.filter(SkiResort.lift_ticket_price_weekend_usd.between(150, 200))
    elif price == "$$$":
        q = q.filter(SkiResort.lift_ticket_price_weekend_usd > 200)


    # Size filter using skiable_acres
    size = request.args.get("size")
    if size and size != "Any":
        if size == "Small":
            q = q.filter(SkiResort.skiable_acres < 1000)
        elif size == "Medium":
            q = q.filter(SkiResort.skiable_acres.between(1000, 5000))
        elif size == "Large":
            q = q.filter(SkiResort.skiable_acres > 5000)

    # Vertical drop filter
    limit = int(request.args.get("drop", 5000))
    if limit < 5000:
        q = q.filter(SkiResort.vertical_drop_ft <= limit)

    # Busiest days filter
    days = request.args.getlist("days")
    if 'Any' not in days and days:
        for day in days:
            q = q.filter(SkiResort.busiest_days.ilike(f"%{day}%"))

    # Snowboarders filter
    snowboard = request.args.get("snowboard")
    if snowboard in ("Yes", "No"):
        q = q.filter(SkiResort.allow_snowboard == (snowboard == "Yes"))

    loc_txt  = request.args.get("location", "").strip()
    radius   = request.args.get("dist", "Any")    # 25 / 100 / 150 / Any
    try:
        origin = geocode(loc_txt) if loc_txt and radius != "Any" else None
        print("loc_txt:", loc_txt, "   radius:", radius)          # 1
        print("origin raw:", origin)                              # 2
        print("provider status:", getattr(origin, 'raw', None))   # 3

    except GeocoderServiceError as e:
        print("⚠️ Could not reach the geocoding service – location filter skipped.")
        origin = None

    if origin and radius != "Any":
        r_mi = int(radius)           # dropdown guarantees int string
        # we can’t slice with SQL unless using PostGIS, so filter in Python
        resorts = []
        for res in q:                # lazily iterates rows that already
                                     # passed the earlier filters
            d = haversine_mi(origin[0], origin[1], res.latitude, res.longitude)
            if d <= r_mi:
                res._distance = round(d)          # keep for template
                resorts.append(res)
    else:
        if loc_txt and not origin:
            print("⚠️ Location not found.")  
        resorts = q.all()


    #resorts = q.all()
    return render_template("search.html", resorts=resorts)


@app.route("/resort/<resort_name>")
def resort(resort_name):
    # Query database using SQLAlchemy model
    readable_name = resort_name.replace("_", " ")

    row = SkiResort.query.filter_by(resort_name=readable_name).first()
    
    if not row:
        abort(404)
        
    # Convert SQLAlchemy model instance to dictionary
    info = {c.name: getattr(row, c.name) for c in row.__table__.columns}
    
    # Get coordinates for weather data
    lat, lon = info["latitude"], info["longitude"]
    
    # Fetch weather data (existing implementation)
    c_now   = current(lat, lon)
    h_next  = hourly(lat, lon)
    d_next  = daily(lat, lon)       
    summary = ski_summary(h_next)
    
    return render_template(
        "resort.html",
        resort=info,
        wx_now=c_now,
        wx_ski=summary,
        wx_daily=d_next,
        owm_key=API_KEY
    )

@app.route("/debug-db")
def debug_db():
    resorts = SkiResort.query.all()
    return f"Found {len(resorts)} resorts: {[r.resort_name for r in resorts]}"


if __name__ == "__main__":
    app.debug = True
    app.run()