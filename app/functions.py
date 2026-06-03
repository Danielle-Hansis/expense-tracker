from model import Expense, Category, User
from flask import render_template, redirect, request
from decimal import Decimal
from extensions import db


# converts string from html to decimal, and checks value
def parse_amount(form_value: str) -> Decimal:
    try:
        value = Decimal(form_value)
    except Exception:
        raise ValueError("Amount must be a number.")

    if value <= 0:
        raise ValueError("Amount must be greater than 0.")

    return value


# converts category_id string into int., and checks value
def parse_category_id(form_value: str) -> int:
    """
    Convert category_id string into int.
    Raises ValueError if invalid.
    """
    try:
        return int(form_value)
    except Exception:
        raise ValueError("Invalid category selected.")

def get_demo_user() -> User:
    user = User.query.filter_by(user_name="demo").first()
    if user is None:
        raise RuntimeError("user not found")
    return user


def expenses_get():
    user = get_demo_user()
    expenses = Expense.query.filter_by(user_id=user.id).order_by(Expense.created).all()
    categories = Category.query.order_by(Category.name).all()
    return render_template("index.html", expenses=expenses, categories=categories)


def expenses_post():
    try:
        amount = parse_amount(request.form.get("amount", "").strip())
        description = request.form.get("description", "").strip()
        category_id = parse_category_id(request.form.get("category_id", ""))
    except ValueError as e:
        # Minimal handling: show the error text (simple + works)
        return str(e), 400

    category = Category.query.get(category_id)
    if category is None:
        return "Category not found", 400

    user = get_demo_user()

    new_entry = Expense(
        amount=amount,
        description=description or None,
        category=category,
        user=user,
    )

    try:
        db.session.add(new_entry)
        db.session.commit()
        return redirect("/expenses")
    except Exception as e:
        db.session.rollback()
        print(f"Exception occurred: {e}")
        return f"Exception occurred: {e}"


def expenses_delete(id:int):
    user = get_demo_user()
    expense = Expense.query.filter_by(id=id, user_id=user.id).first_or_404()
    try:
        db.session.delete(expense)
        db.session.commit()
        return redirect("/expenses")
    except Exception as e:
        db.session.rollback()
        print(f"Exception occurred: {e}")
        return f"Exception occurred: {e}"


def expenses_edit(id: int):
    user = get_demo_user()
    expense = Expense.query.filter_by(id=id, user_id=user.id).first_or_404()

    if request.method == "GET":
        categories = Category.query.order_by(Category.name).all()
        return render_template("edit.html", expense=expense, categories=categories)

    try:
        amount = parse_amount(request.form.get("amount"))
        description = request.form.get("description", "").strip()
        category_id = parse_category_id(request.form.get("category_id"))
    except ValueError as e:
        categories = Category.query.order_by(Category.name).all()
        return render_template("edit.html", expense=expense, categories=categories, error=str(e)), 400

    try:
        category = Category.query.get(category_id)
        if category is None:
            categories = Category.query.order_by(Category.name).all()
            return render_template("edit.html", expense=expense, categories=categories, error="Category not found"), 400

        expense.amount = amount
        expense.description = description or None
        expense.category = category

        db.session.commit()
        return redirect("/expenses")

    except Exception as e:
        db.session.rollback()
        print(f"Exception occurred: {e}")
        return f"Exception occurred: {e}", 500
