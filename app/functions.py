from model import Expense, Category, User
from flask import render_template, redirect, request
from decimal import Decimal
from extensions import db


def expenses_get():
    expenses = Expense.query.order_by(Expense.created).all()
    categories = Category.query.order_by(Category.name).all()
    return render_template("index.html", expenses=expenses, categories=categories)


def expenses_post():
    amount = Decimal(request.form["amount"])
    description = request.form.get("description", "").strip()
    category_id = int(request.form["category_id"])

    category = Category.query.get(category_id)
    if category is None:
        return "Category not found", 400

    #  TODO: receive user details
    new_entry = Expense(amount=amount, description=description or None,
                        category=category)

    try:
        db.session.add(new_entry)
        db.session.commit()
        return redirect("/expenses")
    except Exception as e:
        print(f"Exception occurred: {e}")
        return f"Exception occurred: {e}"


def expenses_delete(id:int):
    expense = Expense.query.get_or_404(id)
    try:
        db.session.delete(expense)
        db.session.commit()
        return redirect("/expenses")
    except Exception as e:
        db.session.rollback()
        print(f"Exception occurred: {e}")
        return f"Exception occurred: {e}"



def expenses_edit(id: int):
    expense = Expense.query.get_or_404(id)

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