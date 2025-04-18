from flask import Flask, render_template  #Q0: What happens if you remove render_template from this line?
app = Flask(__name__)
import pandas as pd

# Load resort data once when the app starts
RESORTS_DF = pd.read_csv('data/resorts/Sample_Ski_Resort_Data.csv')

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
    # Clean up name to match CSV format
    clean_name = resort_name.replace('_', ' ')
    resort_data = RESORTS_DF[RESORTS_DF['resort_name'] == clean_name]
    
    if resort_data.empty:
        abort(404)
    
    # Convert DataFrame row to dictionary
    resort_info = resort_data.iloc[0].to_dict()
    return render_template('resort.html', resort=resort_info)

if __name__ == "__main__":
    app.debug = True
    app.run()