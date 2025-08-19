from flask import Flask
from flask import render_template
import sass # libsass: compiles SCSS → CSS without needing Flask-Scss
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # tells flask where to find files to run app
# reads all .scss files in static/ and Writes compiled .css into the same static/ folder
sass.compile(dirname=('static', 'static'), output_style='expanded')

# sqlalchemy setup:
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


# Model - row of data (for an item)
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Expense {self.id}"


@app.route('/')  # the main route
def index():
    return render_template("index.html")


# Create the tables once before the first run (needs an app context)
with app.app_context():
    db.create_all()
    # Optional: print where the DB actually is, for your sanity check
    print("DB path:", db.engine.url.database)
app.run(debug=True)
