from flask import Flask, render_template  #Q0: What happens if you remove render_template from this line?
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html', user="Test Test")

@app.route("/explore")
def explore():
    resorts = {"Aspen1", "Aspen2", "Aspen3"}
    return render_template('explore.html', collection=resorts)

if __name__ == "__main__":
    app.debug = True
    app.run()