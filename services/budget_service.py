from database import get_connection


def set_budget(user_id, category, amount, month, year):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO budgets (user_id, category, amount, month, year)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id, category, month, year)
        DO UPDATE SET amount=excluded.amount
    """, (user_id, category, amount, month, year))

    conn.commit()
    conn.close()


def get_budgets(user_id, month, year):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, amount
        FROM budgets
        WHERE user_id=? AND month=? AND year=?
    """, (user_id, month, year))

    rows = cursor.fetchall()
    conn.close()

    return {row["category"]: row["amount"] for row in rows}