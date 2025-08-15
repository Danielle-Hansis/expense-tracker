from flask import Flask
from flask import render_template
import sass # libsass: compiles SCSS → CSS without needing Flask-Scss
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # tells flask where to find files to run app
# reads all .scss files in static/ and Writes compiled .css into the same static/ folder
sass.compile(dirname=('static', 'static'), output_style='expanded')


@app.route('/')  # the main route
def index():
    return render_template("index.html")


if __name__ == "__main__":
    # debug=True auto-reloads when you save changes
    app.run(debug=True)
