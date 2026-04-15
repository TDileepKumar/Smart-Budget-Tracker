from datetime import datetime


def build_assistant_response(question, transactions, budgets=None):
    if not transactions:
        return "No transaction data available."

    question = question.lower().strip()

    total_income = sum(float(t["amount"]) for t in transactions if t["type"] == "income")
    total_expense = sum(float(t["amount"]) for t in transactions if t["type"] == "expense")
    balance = total_income - total_expense

    current_month = datetime.now().month
    current_year = datetime.now().year

    monthly_income = 0.0
    monthly_expense = 0.0

    category_spending = {}
    months = set()

    for t in transactions:
        dt = datetime.strptime(t["date"], "%Y-%m-%d %H:%M:%S")
        months.add((dt.year, dt.month))

        amount = float(t["amount"])

        if t["type"] == "income":
            if dt.month == current_month and dt.year == current_year:
                monthly_income += amount
        elif t["type"] == "expense":
            category_spending[t["category"]] = category_spending.get(t["category"], 0) + amount
            if dt.month == current_month and dt.year == current_year:
                monthly_expense += amount

    monthly_balance = monthly_income - monthly_expense
    avg_expense = total_expense / len(months) if months else 0.0
    top_category = max(category_spending, key=category_spending.get) if category_spending else None

    if "highest spending category" in question or "top spending category" in question:
        if top_category:
            return f"Your highest spending category is {top_category} with ₹{category_spending[top_category]:.2f}."
        return "No expense data available."

    elif "which category" in question and "spend" in question:
        if top_category:
            return f"You spend the most on {top_category}. Consider reducing it."
        return "No expense category data available."

    elif "this month" in question and "spend" in question:
        return f"You spent ₹{monthly_expense:.2f} this month."

    elif "monthly expense" in question:
        return f"Your expense this month is ₹{monthly_expense:.2f}."

    elif "monthly income" in question:
        return f"Your income this month is ₹{monthly_income:.2f}."

    elif "monthly balance" in question or "monthly summary" in question:
        return (
            f"This month: income ₹{monthly_income:.2f}, "
            f"expense ₹{monthly_expense:.2f}, "
            f"balance ₹{monthly_balance:.2f}."
        )

    elif "total income" in question:
        return f"Your total income is ₹{total_income:.2f}."

    elif "total expense" in question:
        return f"Your total expense is ₹{total_expense:.2f}."

    elif question == "income":
        return f"Your total income is ₹{total_income:.2f}."

    elif question == "expense":
        return f"Your total expense is ₹{total_expense:.2f}."

    elif "balance" in question:
        return f"Your current balance is ₹{balance:.2f}."

    elif "average" in question and "expense" in question:
        return f"Your average monthly expense is ₹{avg_expense:.2f}."

    elif "save" in question or "saving" in question:
        return f"You have saved ₹{balance:.2f}."

    elif "budget" in question and "advice" in question:
        return "Set realistic budgets and track overspending categories regularly."

    elif "budget" in question and budgets:
        exceeded = []
        for cat, budget in budgets.items():
            spent = category_spending.get(cat, 0)
            if spent > budget:
                exceeded.append(cat)

        if exceeded:
            return f"You exceeded budget in: {', '.join(exceeded)}."
        return "You are within all budgets."

    elif "suggest" in question or "improve" in question or "reduce" in question:
        if top_category:
            return (
                f"To reduce expenses, focus first on {top_category}, "
                f"because it is your highest spending category."
            )
        return "To reduce expenses, review your highest spending areas and set stricter budgets."

    return "AI_FALLBACK"