from database import get_connection


def add_transaction_db(user_id, title, amount, category, t_type, date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (user_id, title, amount, category, type, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, title, amount, category, t_type, date))

    conn.commit()
    conn.close()


def get_all_transactions_db(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM transactions
        WHERE user_id = ?
        ORDER BY date DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def delete_transaction_db(transaction_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM transactions
        WHERE id = ? AND user_id = ?
    """, (transaction_id, user_id))

    conn.commit()
    conn.close()


def update_transaction_db(transaction_id, user_id, title, amount, category, t_type):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET title=?, amount=?, category=?, type=?
        WHERE id=? AND user_id=?
    """, (title, amount, category, t_type, transaction_id, user_id))

    conn.commit()
    conn.close()


def get_transaction_by_id_db(transaction_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM transactions
        WHERE id=? AND user_id=?
    """, (transaction_id, user_id))

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None