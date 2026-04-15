from datetime import datetime


def calculate_summary(transactions):
    income = sum(float(t["amount"]) for t in transactions if t["type"] == "income")
    expense = sum(float(t["amount"]) for t in transactions if t["type"] == "expense")
    balance = income - expense
    return round(income, 2), round(expense, 2), round(balance, 2)


def calculate_monthly_summary(transactions):
    now = datetime.now()
    filtered = []

    for t in transactions:
        try:
            tx_date = datetime.strptime(t["date"], "%Y-%m-%d %H:%M:%S")
            if tx_date.month == now.month and tx_date.year == now.year:
                filtered.append(t)
        except (KeyError, ValueError):
            continue

    return calculate_summary(filtered)


def get_expense_chart_data(transactions):
    category_data = {}

    for t in transactions:
        if t["type"] == "expense":
            category = t["category"]
            amount = float(t["amount"])
            category_data[category] = category_data.get(category, 0) + amount

    labels = list(category_data.keys())
    values = list(category_data.values())
    return labels, values


def get_monthly_trend_data(transactions):
    monthly_data = {}

    for t in transactions:
        try:
            tx_date = datetime.strptime(t["date"], "%Y-%m-%d %H:%M:%S")
            month_key = tx_date.strftime("%b %Y")
        except (KeyError, ValueError):
            continue

        if month_key not in monthly_data:
            monthly_data[month_key] = {"income": 0.0, "expense": 0.0}

        amount = float(t["amount"])
        if t["type"] == "income":
            monthly_data[month_key]["income"] += amount
        elif t["type"] == "expense":
            monthly_data[month_key]["expense"] += amount

    sorted_items = sorted(
        monthly_data.items(),
        key=lambda item: datetime.strptime(item[0], "%b %Y")
    )

    labels = [item[0] for item in sorted_items]
    income_values = [round(item[1]["income"], 2) for item in sorted_items]
    expense_values = [round(item[1]["expense"], 2) for item in sorted_items]

    return labels, income_values, expense_values


def get_top_spending_category(transactions):
    category_totals = {}

    for t in transactions:
        if t["type"] == "expense":
            category = t["category"]
            amount = float(t["amount"])
            category_totals[category] = category_totals.get(category, 0) + amount

    if not category_totals:
        return None, 0.0

    top_category = max(category_totals, key=category_totals.get)
    return top_category, round(category_totals[top_category], 2)