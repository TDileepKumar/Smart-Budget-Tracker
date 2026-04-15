from flask import Blueprint, render_template, request, redirect, url_for, session, Response
from datetime import datetime
import csv
import io

from services.budget_service import set_budget, get_budgets
from services.auth_service import create_user, login_user
from services.analytics_service import (
    calculate_summary,
    calculate_monthly_summary,
    get_expense_chart_data,
    get_monthly_trend_data,
    get_top_spending_category,
)
from services.assistant_service import build_assistant_response
from services.db_service import (
    add_transaction_db,
    get_all_transactions_db,
    get_transaction_by_id_db,
    update_transaction_db,
    delete_transaction_db,
)

main = Blueprint("main", __name__)

INCOME_CATEGORIES = [
    "Salary", "Freelance", "Business", "Bonus", "Investment", "Other Income"
]

EXPENSE_CATEGORIES = [
    "Food", "Travel", "Bills", "Shopping", "Rent",
    "Entertainment", "Health", "Education", "Other Expense"
]


@main.route("/signup", methods=["GET", "POST"])
def signup():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not email or not password:
            error = "All fields are required."
        elif create_user(username, email, password):
            return redirect(url_for("main.login"))
        else:
            error = "User already exists or signup failed."

    return render_template("signup.html", error=error)


@main.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        user = login_user(email, password)

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("main.dashboard"))
        else:
            error = "Invalid credentials."

    return render_template("login.html", error=error)


@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))


@main.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("main.login"))
    return render_template("index.html")


@main.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    error_message = None

    if request.method == "POST":
        budget_category = request.form.get("budget_category", "").strip()
        budget_amount = request.form.get("budget_amount", "").strip()

        if budget_category and budget_amount:
            try:
                budget_value = float(budget_amount)
                if budget_value <= 0:
                    error_message = "Budget amount must be greater than zero."
                else:
                    set_budget(
                        user_id,
                        budget_category,
                        budget_value,
                        datetime.now().month,
                        datetime.now().year
                    )
                    return redirect(url_for("main.dashboard"))
            except ValueError:
                error_message = "Invalid budget amount."
        else:
            title = request.form.get("title", "").strip()
            amount_raw = request.form.get("amount", "").strip()
            category = request.form.get("category", "").strip()
            transaction_type = request.form.get("type", "").strip().lower()

            if not title:
                error_message = "Description cannot be empty."
            elif transaction_type not in ["income", "expense"]:
                error_message = "Invalid transaction type selected."
            elif not category:
                error_message = "Category is required."
            else:
                try:
                    amount = round(float(amount_raw), 2)
                    if amount <= 0:
                        error_message = "Amount must be greater than zero."
                except ValueError:
                    error_message = "Please enter a valid amount."

            if error_message is None:
                add_transaction_db(
                    user_id,
                    title,
                    amount,
                    category,
                    transaction_type,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                return redirect(url_for("main.dashboard"))

    transactions = get_all_transactions_db(user_id)
    recent_transactions = transactions[:5]

    total_income, total_expense, balance = calculate_summary(transactions)
    monthly_income, monthly_expense, monthly_balance = calculate_monthly_summary(transactions)
    chart_labels, chart_values = get_expense_chart_data(transactions)

    budgets = get_budgets(user_id, datetime.now().month, datetime.now().year)

    category_spending = {}
    for t in transactions:
        if t["type"] == "expense":
            category_spending[t["category"]] = category_spending.get(t["category"], 0) + float(t["amount"])

    budget_status = []
    for category, budget in budgets.items():
        spent = category_spending.get(category, 0)
        remaining = budget - spent
        budget_status.append({
            "category": category,
            "budget": budget,
            "spent": spent,
            "remaining": remaining
        })

    return render_template(
        "dashboard.html",
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        monthly_income=monthly_income,
        monthly_expense=monthly_expense,
        monthly_balance=monthly_balance,
        chart_labels=chart_labels,
        chart_values=chart_values,
        income_categories=INCOME_CATEGORIES,
        expense_categories=EXPENSE_CATEGORIES,
        error_message=error_message,
        recent_transactions=recent_transactions,
        budget_status=budget_status
    )


@main.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    transactions = get_all_transactions_db(user_id)

    selected_type = request.args.get("type", "").strip()
    selected_category = request.args.get("category", "").strip()
    search_query = request.args.get("search", "").strip().lower()

    if selected_type:
        transactions = [t for t in transactions if t["type"] == selected_type]

    if selected_category:
        transactions = [t for t in transactions if t["category"] == selected_category]

    if search_query:
        transactions = [
            t for t in transactions
            if search_query in t["title"].lower()
            or search_query in t["category"].lower()
            or search_query in t["type"].lower()
            or search_query in t["date"].lower()
        ]

    return render_template(
        "history.html",
        transactions=transactions,
        selected_type=selected_type,
        selected_category=selected_category,
        search_query=search_query
    )


@main.route("/history/export")
def export_history_csv():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    transactions = get_all_transactions_db(user_id)

    selected_type = request.args.get("type", "").strip()
    selected_category = request.args.get("category", "").strip()
    search_query = request.args.get("search", "").strip().lower()

    if selected_type:
        transactions = [t for t in transactions if t["type"] == selected_type]

    if selected_category:
        transactions = [t for t in transactions if t["category"] == selected_category]

    if search_query:
        transactions = [
            t for t in transactions
            if search_query in t["title"].lower()
            or search_query in t["category"].lower()
            or search_query in t["type"].lower()
            or search_query in t["date"].lower()
        ]

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Title", "Type", "Category", "Amount", "Date"])

    for t in transactions:
        writer.writerow([
            t["id"],
            t["title"],
            t["type"],
            t["category"],
            f'{float(t["amount"]):.2f}',
            t["date"]
        ])

    csv_data = output.getvalue()
    output.close()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"}
    )


@main.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_transaction(id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    transaction = get_transaction_by_id_db(id, user_id)

    if not transaction:
        return "Transaction not found"

    error_message = None

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        amount_raw = request.form.get("amount", "").strip()
        category = request.form.get("category", "").strip()
        transaction_type = request.form.get("type", "").strip().lower()

        if not title:
            error_message = "Description cannot be empty."
        elif not category:
            error_message = "Category is required."
        else:
            try:
                amount = round(float(amount_raw), 2)
                if amount <= 0:
                    error_message = "Amount must be greater than zero."
            except ValueError:
                error_message = "Please enter a valid amount."

        if error_message is None:
            update_transaction_db(id, user_id, title, amount, category, transaction_type)
            return redirect(url_for("main.history"))

    return render_template(
        "edit.html",
        transaction=transaction,
        income_categories=INCOME_CATEGORIES,
        expense_categories=EXPENSE_CATEGORIES,
        error_message=error_message
    )


@main.route("/delete/<int:id>", methods=["POST"])
def delete_transaction(id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    delete_transaction_db(id, user_id)
    return redirect(url_for("main.history"))


@main.route("/analytics")
def analytics():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    transactions = get_all_transactions_db(user_id)

    total_income, total_expense, balance = calculate_summary(transactions)
    monthly_income, monthly_expense, monthly_balance = calculate_monthly_summary(transactions)

    expense_labels, expense_values = get_expense_chart_data(transactions)
    trend_labels, income_values, expense_trend_values = get_monthly_trend_data(transactions)
    top_category, top_amount = get_top_spending_category(transactions)

    return render_template(
        "analytics.html",
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        monthly_income=monthly_income,
        monthly_expense=monthly_expense,
        monthly_balance=monthly_balance,
        expense_labels=expense_labels,
        expense_values=expense_values,
        trend_labels=trend_labels,
        income_values=income_values,
        expense_trend_values=expense_trend_values,
        top_category=top_category,
        top_amount=top_amount,
        transaction_count=len(transactions)
    )


@main.route("/assistant")
def assistant():
    if "user_id" not in session:
        return redirect(url_for("main.login"))
    return render_template("assistant.html")


@main.route("/ask", methods=["POST"])
def ask():
    if "user_id" not in session:
        return "Please login first."

    user_id = session["user_id"]
    question = request.form.get("question", "").strip().lower()

    if not question:
        return "Please ask a valid question."

    transactions = get_all_transactions_db(user_id)
    budgets = get_budgets(
        user_id,
        datetime.now().month,
        datetime.now().year
    )

    response = build_assistant_response(question, transactions, budgets)

    if response == "AI_FALLBACK":
        return (
            "I can help with:\n"
            "- Income and expense tracking\n"
            "- Balance and savings\n"
            "- Monthly analysis\n"
            "- Budget usage and overspending\n"
            "- Spending insights"
        )

    return response