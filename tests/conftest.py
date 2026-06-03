"""
import pytest
from app import create_app
from extensions import db
from model import Category


@pytest.fixture()
def app(tmp_path):
    # Create a temporary SQLite file path for this test run
    test_db_path = tmp_path / "test.db"

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{test_db_path}",
    })

    # Create tables + seed data for this test app
    with app.app_context():
        db.create_all()

        # Ensure categories exist (seed function should do it, but this makes tests robust)
        if Category.query.count() == 0:
            from model import seed_default_categories, seed_default_user
            seed_default_categories()
            seed_default_user()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def any_category_id(app) -> int:
    with app.app_context():
        category = Category.query.order_by(Category.id).first()
        return category.id
"""

"""
app.py should be an application factory:

BASE_DIR = Path(__file__).resolve().parent.parent


def create_app(config_overrides: dict | None = None) -> Flask:
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )

    # Default config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

    # Test config overrides (if provided)
    if config_overrides:
        app.config.update(config_overrides)

    # Compile SCSS only when not testing (keeps tests fast and avoids extra noise)
    if not app.config.get("TESTING", False):
        sass.compile(dirname=("static", "static"), output_style="expanded")

    db.init_app(app)

    with app.app_context():
        db.create_all()
        seed_default_categories()
        seed_default_user()

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

    @app.route("/expenses/<int:id>/edit", methods=["GET", "POST"])
    def expenses_edit_route(id: int):
        return functions.expenses_edit(id)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
"""
