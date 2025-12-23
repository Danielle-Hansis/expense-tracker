from model import Expense, Category, User
from flask import render_template, redirect, request
from decimal import Decimal
from extensions import db


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
    amount = Decimal(request.form["amount"])
    description = request.form.get("description", "").strip()
    category_id = int(request.form["category_id"])

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
        amount = Decimal(request.form["amount"])
        description = request.form.get("description", "").strip()
        category_id = int(request.form["category_id"])

        category = Category.query.get(category_id)
        if category is None:
            return "Category not found", 400

        expense.amount = amount
        expense.description = description or None  # store NULL instead of empty string
        expense.category = category                # sets expense.category_id under the hood

        db.session.commit()
        return redirect("/expenses")

    except Exception as e:
        # If anything fails mid-transaction, undo partial work
        db.session.rollback()
        print(f"Exception occurred: {e}")
        return f"Exception occurred: {e}", 500