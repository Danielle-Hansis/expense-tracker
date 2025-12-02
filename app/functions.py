from model import Expense, Category, User
from flask import render_template, redirect, request
from decimal import Decimal
from extensions import db


def index():
    if request.method == "POST":
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
            return redirect("/")
        except Exception as e:
            print(f"Exception occurred: {e}")
            return f"Exception occurred: {e}"

    else:
        expenses = Expense.query.order_by(Expense.created).all()
        categories = Category.query.order_by(Category.name).all()
        return render_template("index.html", expenses=expenses, categories=categories)


def delete(id:int):
    expense = Expense.query.get_or_404(id)
    try:
        db.session.delete(expense)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"Exception occurred: {e}")
        return f"Exception occurred: {e}"

