
from database import get_connection


def add_agent(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO agents (name)
        VALUES (?)
    """, (name.strip(),))

    conn.commit()
    agent_id = cursor.lastrowid
    conn.close()

    return f"Agent registered successfully! ID: {agent_id}"


def get_agents():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT agent_id, name, availability
        FROM agents
        ORDER BY agent_id
    """)

    agents = cursor.fetchall()
    conn.close()

    return agents


def update_agent_status(agent_id, status):
    if status not in ["Available", "Busy"]:
        return "Invalid agent status!"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE agents
        SET availability = ?
        WHERE agent_id = ?
    """, (status, agent_id))

    updated = cursor.rowcount
    conn.commit()
    conn.close()

    return (
        "Agent status updated successfully!"
        if updated else "Agent not found!"
    )
