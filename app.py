from flask import Flask
from flask import render_template
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # tells flask where to find files to run app


@app.route('/')  # the main route
def index():
    return render_template('index.html')


if __name__ == "__main__":
    # debug=True auto-reloads when you save changes
    app.run(debug=True)
