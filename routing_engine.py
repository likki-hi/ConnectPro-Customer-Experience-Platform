
from database import get_connection


# Priority ranking
PRIORITY_RANK = {
    "High": 3,
    "Medium": 2,
    "Low": 1
}

# Sentiment ranking
SENTIMENT_RANK = {
    "Negative": 3,
    "Neutral": 2,
    "Positive": 1
}


# Get unassigned customer contacts
def get_routing_queue():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.contact_id,
               cu.name,
               c.issue,
               c.priority,
               c.sentiment,
               c.sentiment_score,
               c.created_at
        FROM contacts c
        JOIN customers cu
        ON c.customer_id = cu.customer_id
        WHERE c.agent_id IS NULL
        AND c.status != 'Resolved'
    """)

    contacts = cursor.fetchall()
    conn.close()

    # Sort by priority, sentiment and creation time
    contacts.sort(
        key=lambda row: (
            PRIORITY_RANK.get(row[3], 0),
            SENTIMENT_RANK.get(row[4], 0),
            row[6] or ""
        ),
        reverse=True
    )

    return contacts


# Assign contact to an available agent
def assign_agent(contact_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT contact_id
            FROM contacts
            WHERE contact_id = ?
            AND agent_id IS NULL
            AND status != 'Resolved'
        """, (contact_id,))

        if cursor.fetchone() is None:
            return "Contact not found or already assigned!"

        # Find an available agent
        cursor.execute("""
            SELECT agent_id, name
            FROM agents
            WHERE availability = 'Available'
            ORDER BY agent_id
            LIMIT 1
        """)

        agent = cursor.fetchone()

        if agent is None:
            return "No agents available!"

        agent_id, agent_name = agent

        # Assign contact
        cursor.execute("""
            UPDATE contacts
            SET agent_id = ?,
                status = 'In Progress'
            WHERE contact_id = ?
            AND agent_id IS NULL
        """, (agent_id, contact_id))

        if cursor.rowcount != 1:
            conn.rollback()
            return "Unable to assign agent!"

        # Mark agent as busy
        cursor.execute("""
            UPDATE agents
            SET availability = 'Busy'
            WHERE agent_id = ?
        """, (agent_id,))

        conn.commit()

        return f"Contact assigned successfully to {agent_name}!"

    except Exception as error:
        conn.rollback()
        return f"Routing error: {error}"

    finally:
        conn.close()


# Automatically route the highest-ranked contact
def route_next_contact():

    queue = get_routing_queue()

    if not queue:
        return "No unassigned contacts available!"

    contact_id = queue[0][0]

    return assign_agent(contact_id)
