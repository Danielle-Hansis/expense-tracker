from flask import Flask, request, redirect, url_for                 # request used by your route
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


@app.get("/")
def home():
    return redirect(url_for("expenses_get_route"))


@app.get("/expenses")
def expenses_get_route():
    return functions.expenses_get()


@app.post("/expenses")
def expenses_post_route():
    return functions.expenses_post()


@app.post("/expenses/<int:id>/delete")
def expenses_delete_route(id: int):
    return functions.expenses_delete(id)


# uses GET to show the form and POST to apply updates
# html forms can't send delete/ patch
@app.route("/expenses/<int:id>/edit", methods=["GET", "POST"])
def expenses_edit_route(id: int):
    return functions.expenses_edit(id)


if __name__ == "__main__":
    app.run(debug=True)

