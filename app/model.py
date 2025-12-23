from datetime import datetime, timezone
from extensions import db


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    created = db.Column(db.DateTime(timezone=True), nullable=False,
                        default=lambda: datetime.now(timezone.utc))
    description = db.Column(db.String(255), nullable=True)

    # foreign keys:
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True) # TODO- change to false, when auth is activated
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    user = db.relationship("User", back_populates="expenses")
    category = db.relationship("Category", back_populates="expenses")

    def __repr__(self) -> str:
        return f"Expense {self.id} amount={self.amount}"


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    expenses = db.relationship("Expense", back_populates="category")
    # One category has many expenses

    def __repr__(self) -> str:
        return f"Category {self.name}"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    expenses = db.relationship("Expense", back_populates="user")
    # A user has many expenses

    def __repr__(self) -> str:
        return f"User {self.user_name}"


# limiting allowed categories, for better analysis abilities-
# A fixed list of allowed category names:
DEFAULT_CATEGORIES = ["Groceries", "Eating Out", "Shopping", "Rent",
    "Utilities", "Internet & Phone", "Transport", "Car - Fuel", "Car - Maintenance",
    "Health", "Insurance", "Subscriptions", "Entertainment", "Travel",
    "Education", "Gifts & Donations", "Household", "Pets", "Other",]


def seed_default_categories():
    """
    Insert the fixed default categories into the database, if they are missing.
    Safe to run multiple times (idempotent).
    """
    for name in DEFAULT_CATEGORIES:
        # See if a category with this name already exists
        existing = Category.query.filter_by(name=name).first()

        if existing is None:
            # If not, create a new Category row
            category = Category(name=name)
            db.session.add(category)
    db.session.commit()


def seed_default_user():
    """
    Insert a single default user into the database if missing.
    Safe to run multiple times (idempotent).
    """
    existing = User.query.filter_by(user_name="demo").first()

    if existing is None:
        user = User(user_name="demo", password="not-used")
        db.session.add(user)

    # Commit all new categories at once
    db.session.commit()
