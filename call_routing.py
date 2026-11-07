
from database import get_connection


def assign_agent(contact_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT contact_id
            FROM contacts
            WHERE contact_id = ?
            AND agent_id IS NULL
        """, (contact_id,))

        if cursor.fetchone() is None:
            return "Contact not found or already assigned!"

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

        cursor.execute("""
            UPDATE contacts
            SET agent_id = ?
            WHERE contact_id = ?
            AND agent_id IS NULL
        """, (agent_id, contact_id))

        if cursor.rowcount == 0:
            return "Unable to assign agent!"

        cursor.execute("""
            UPDATE agents
            SET availability = 'Busy'
            WHERE agent_id = ?
        """, (agent_id,))

        conn.commit()

        return f"Contact successfully assigned to {agent_name}!"

    except Exception as error:
        conn.rollback()
        return f"Routing error: {error}"

    finally:
        conn.close()
