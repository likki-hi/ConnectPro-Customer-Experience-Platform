
from database import get_connection


def add_customer(name, email, phone):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT customer_id
            FROM customers
            WHERE LOWER(email) = LOWER(?)
        """, (email.strip(),))

        if cursor.fetchone():
            return "Customer already exists!"

        cursor.execute("""
            INSERT INTO customers (name, email, phone)
            VALUES (?, ?, ?)
        """, (name.strip(), email.strip(), phone.strip()))

        conn.commit()
        customer_id = cursor.lastrowid

        return f"Customer registered successfully! ID: {customer_id}"

    except Exception as error:
        return f"Error: {error}"

    finally:
        conn.close()


def get_customers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT customer_id, name, email, phone
        FROM customers
        ORDER BY customer_id DESC
    """)

    customers = cursor.fetchall()
    conn.close()

    return customers
