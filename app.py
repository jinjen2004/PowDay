from flask import Flask, render_template  #Q0: What happens if you remove render_template from this line?
app = Flask(__name__)

import pandas as pd
import os, time, requests, functools, time 
from typing import Dict, Any, List 
from weather import current, hourly, daily, ski_summary

# Load resort data once when the app starts
RESORTS_DF = pd.read_csv('data/resorts/Sample_Ski_Resort_Data.csv')

# Our weather API
BASE = "https://api.openweathermap.org/data"
API_KEY = "6a8dc08d5123e7c104b59aa3b4c138d1" # <- terrible practice o well

@app.route("/")
def home():
    return render_template('home.html', user="Test Test")

@app.route("/explore")
def explore():
    resorts = [["Vail", "this is a cool resort"], ["Breckenridge", "really hard"], ["ParkCity", "awesome awesome awesome"]]
    return render_template('explore.html', collection=resorts)
    # The images are referenced by the resort name and are in the static/img folder. Works for now but might not be the best system, storing the image path may be better.

@app.route("/search")
def search():
    return render_template('search.html')

@app.route("/resort/<resort_name>")
def resort(resort_name):
    clean = resort_name.replace('_', ' ')
    row = RESORTS_DF[RESORTS_DF['resort_name'] == clean]
    if row.empty: abort(404)
    info = row.iloc[0].to_dict()

    lat, lon = info["latitude"], info["longitude"]
    c_now   = current(lat, lon)
    h_next  = hourly(lat, lon)
    d_next  = daily(lat, lon)       
    summary = ski_summary(h_next)

    # after assembling wx_now / wx_daily ...
    return render_template(
        "resort.html",
        resort=info,
        wx_now=c_now,
        wx_ski=summary,
        wx_daily=d_next,             # <-- needed for 5‑day table
        owm_key=API_KEY  # <-- for tile layer
    )

if __name__ == "__main__":
    app.debug = True
    app.run()