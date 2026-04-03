from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"transactions": []}

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def calculate_summary(transactions):
    total_income = 0
    total_expense = 0

    for transaction in transactions:
        amount = float(transaction["amount"])

        if transaction["type"] == "income":
            total_income += amount
        else:
            total_expense += amount

    balance = total_income - total_expense
    return total_income, total_expense, balance


def get_expense_chart_data(transactions):
    category_totals = {}

    for transaction in transactions:
        if transaction["type"] == "expense":
            category = transaction["category"]
            amount = float(transaction["amount"])

            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    return labels, values


@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()

    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]
        category = request.form["category"]
        transaction_type = request.form["type"]

        new_transaction = {
            "id": int(datetime.now().timestamp() * 1000),
            "title": title,
            "amount": amount,
            "category": category,
            "type": transaction_type,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        data["transactions"].append(new_transaction)
        save_data(data)

        return redirect(url_for("index"))

    transactions = data["transactions"]
    total_income, total_expense, balance = calculate_summary(transactions)
    chart_labels, chart_values = get_expense_chart_data(transactions)

    return render_template(
        "index.html",
        transactions=transactions,
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        chart_labels=chart_labels,
        chart_values=chart_values
    )


@app.route("/delete/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    data = load_data()

    data["transactions"] = [
        transaction for transaction in data["transactions"]
        if transaction["id"] != transaction_id
    ]

    save_data(data)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)