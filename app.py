from flask import Flask, render_template  #Q0: What happens if you remove render_template from this line?
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html', user="Test Test")

if __name__ == "__main__":
    app.debug = True
    app.run()