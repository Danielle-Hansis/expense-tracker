from sqlalchemy import Integer, String, Numeric, DateTime
from datetime import datetime, timezone
from extensions import db


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), default="No Category")
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    created = db.Column(db.DateTime(timezone=True), nullable=False,
                        default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"Expense {self.id}"

