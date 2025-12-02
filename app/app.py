from flask import Flask, request                    # request used by your route
import sass                                         # compiles SCSS → CSS
from extensions import db                          # <-- import the unbound SQLAlchemy instance
from pathlib import Path
from model import seed_default_categories
import functions


BASE_DIR = Path(__file__).resolve().parent.parent  # project root (one level above /app)
app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)
sass.compile(dirname=('static', 'static'), output_style='expanded')

# --- DB setup ---
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)                                    # <-- bind db to this app (replaces SQLAlchemy(app))

# Create tables AFTER models are imported, inside an app context
with app.app_context():                                 # <-- ensures Expense is registered with SQLAlchemy
    db.create_all()
    seed_default_categories()
    print("DB path:", db.engine.url.database)


@app.route("/", methods=["POST", "GET"])
def index_route():
    return functions.index()


@app.route("/delete/<int:id>")
def delete_route(id: int):
    return functions.delete(id)


if __name__ == "__main__":
    app.run(debug=True)

