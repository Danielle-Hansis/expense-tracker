from model import Expense
from flask import render_template, redirect, request
from decimal import Decimal
from extensions import db


def index():
    if request.method == "POST":
        category = request.form["category"]
        amount = Decimal(request.form["amount"])
        new_entry = Expense(category=category, amount=amount)
        try:
            db.session.add(new_entry)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Exception occurred: {e}")
            return f"Exception occurred: {e}"

    else:
        expenses = Expense.query.order_by(Expense.created).all()
        return render_template("index.html", expenses=expenses)


def delete(id:int):
    expense = Expense.query.get_or_404(id)
    try:
        db.session.delete(expense)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"Exception occurred: {e}")
        return f"Exception occurred: {e}"

