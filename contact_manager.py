
from database import get_connection
from sentiment_analyzer import analyze_sentiment


# Register a new customer contact
def add_contact(customer_id, issue, priority="Medium", channel="Voice"):

    # Analyze customer message
    result = analyze_sentiment(issue)

    sentiment = result["sentiment"]
    score = result["score"]

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO contacts
            (customer_id, issue, channel, priority,
             sentiment, sentiment_score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            customer_id,
            issue,
            channel,
            priority,
            sentiment,
            score
        ))

        conn.commit()

        contact_id = cursor.lastrowid

        return (
            f"Contact registered successfully! ID: {contact_id}\n"
            f"Sentiment: {sentiment}\n"
            f"Sentiment Score: {score}"
        )

    except Exception as error:
        return f"Error: {error}"

    finally:
        conn.close()


# Get all contacts
def get_contacts():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT contact_id, customer_id, agent_id, issue,
               channel, priority, status, created_at,
               sentiment, sentiment_score
        FROM contacts
        ORDER BY contact_id DESC
    """)

    contacts = cursor.fetchall()
    conn.close()

    return contacts


# Get contacts with customer and agent names
def get_contact_details():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.contact_id, cu.name, a.name, c.issue,
               c.channel, c.priority, c.status, c.created_at,
               c.sentiment, c.sentiment_score
        FROM contacts c
        JOIN customers cu
        ON c.customer_id = cu.customer_id
        LEFT JOIN agents a
        ON c.agent_id = a.agent_id
        ORDER BY c.contact_id DESC
    """)

    records = cursor.fetchall()
    conn.close()

    return records


# Update contact status
def update_contact_status(contact_id, status):

    allowed_statuses = ["Open", "In Progress", "Resolved"]

    if status not in allowed_statuses:
        return "Invalid status!"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT agent_id
        FROM contacts
        WHERE contact_id = ?
    """, (contact_id,))

    contact = cursor.fetchone()

    if contact is None:
        conn.close()
        return "Contact not found!"

    agent_id = contact[0]

    cursor.execute("""
        UPDATE contacts
        SET status = ?
        WHERE contact_id = ?
    """, (status, contact_id))

    # Make agent available if no other active contacts remain
    if status == "Resolved" and agent_id is not None:

        cursor.execute("""
            SELECT COUNT(*)
            FROM contacts
            WHERE agent_id = ?
            AND status != 'Resolved'
        """, (agent_id,))

        active_contacts = cursor.fetchone()[0]

        if active_contacts == 0:
            cursor.execute("""
                UPDATE agents
                SET availability = 'Available'
                WHERE agent_id = ?
            """, (agent_id,))

    conn.commit()
    conn.close()

    return "Contact status updated successfully!"


# IVR menu simulation
def ivr_menu():

    print("\nWelcome to Customer Support")

    print("1. Technical Support")
    print("2. Billing Support")
    print("3. Order Support")

    choice = input("Enter your choice: ")

    categories = {
        "1": "Technical Support",
        "2": "Billing Support",
        "3": "Order Support"
    }

    return categories.get(choice)
