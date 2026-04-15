from datetime import datetime


def build_assistant_response(question, transactions, budgets=None):
    if not transactions:
        return "No transaction data available."

    question = question.lower()

    total_income = sum(float(t["amount"]) for t in transactions if t["type"] == "income")
    total_expense = sum(float(t["amount"]) for t in transactions if t["type"] == "expense")
    balance = total_income - total_expense

    current_month = datetime.now().month
    current_year = datetime.now().year

    monthly_expense = sum(
        float(t["amount"])
        for t in transactions
        if t["type"] == "expense"
        and datetime.strptime(t["date"], "%Y-%m-%d %H:%M:%S").month == current_month
        and datetime.strptime(t["date"], "%Y-%m-%d %H:%M:%S").year == current_year
    )

    # Category spending
    category_spending = {}
    for t in transactions:
        if t["type"] == "expense":
            category_spending[t["category"]] = category_spending.get(t["category"], 0) + float(t["amount"])

    top_category = max(category_spending, key=category_spending.get) if category_spending else None

    # Average expense
    months = set()
    for t in transactions:
        dt = datetime.strptime(t["date"], "%Y-%m-%d %H:%M:%S")
        months.add((dt.year, dt.month))

    avg_expense = total_expense / len(months) if months else 0

    # ---------------- RESPONSES ---------------- #

    if "highest" in question or "top category" in question:
        if top_category:
            return f"Your highest spending category is {top_category} with ₹{category_spending[top_category]:.2f}."
        return "No expense data available."

    elif "monthly expense" in question:
        return f"Your expense this month is ₹{monthly_expense:.2f}."

    elif "balance" in question:
        return f"Your current balance is ₹{balance:.2f}."

    elif "income" in question:
        return f"Your total income is ₹{total_income:.2f}."

    elif "expense" in question:
        return f"Your total expense is ₹{total_expense:.2f}."

    elif "average" in question:
        return f"Your average monthly expense is ₹{avg_expense:.2f}."

    elif "save" in question or "saving" in question:
        return f"You have saved ₹{balance:.2f}."

    elif "budget" in question and budgets:
        exceeded = []
        for cat, budget in budgets.items():
            spent = category_spending.get(cat, 0)
            if spent > budget:
                exceeded.append(cat)

        if exceeded:
            return f"You exceeded budget in: {', '.join(exceeded)}."
        return "You are within all budgets."

    else:
        return "I can help with income, expense, balance, savings, monthly analysis, and budget insights."

def generate_summary(transactions):
    total_income = sum(float(t["amount"]) for t in transactions if t["type"] == "income")
    total_expense = sum(float(t["amount"]) for t in transactions if t["type"] == "expense")
    balance = total_income - total_expense

    return f"""
Total Income: ₹{total_income:.2f}
Total Expense: ₹{total_expense:.2f}
Balance: ₹{balance:.2f}
"""