from database import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


def create_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        """, (username, email, generate_password_hash(password)))

        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user["password"], password):
        return dict(user)

    return None