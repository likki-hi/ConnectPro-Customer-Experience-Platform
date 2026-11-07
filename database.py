
import sqlite3

DB_NAME = "amazon_connect.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # Create Customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT
        )
    """)

    # Create Agents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            agent_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            availability TEXT DEFAULT 'Available'
        )
    """)

    # Create Contacts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            agent_id INTEGER,
            issue TEXT NOT NULL,
            channel TEXT DEFAULT 'Voice',
            priority TEXT DEFAULT 'Medium',
            status TEXT DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sentiment TEXT DEFAULT 'Neutral',
            sentiment_score REAL DEFAULT 0,

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id),

            FOREIGN KEY (agent_id)
                REFERENCES agents(agent_id)
        )
    """)

    # Check existing database columns
    cursor.execute("PRAGMA table_info(contacts)")
    columns = [column[1] for column in cursor.fetchall()]

    # Add sentiment column if missing
    if "sentiment" not in columns:
        cursor.execute("""
            ALTER TABLE contacts
            ADD COLUMN sentiment TEXT DEFAULT 'Neutral'
        """)

    # Add sentiment score column if missing
    if "sentiment_score" not in columns:
        cursor.execute("""
            ALTER TABLE contacts
            ADD COLUMN sentiment_score REAL DEFAULT 0
        """)

    # Create index
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_contacts_status
        ON contacts(status)
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database tables created/updated successfully!")
