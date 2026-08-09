from app.database.database import get_connection


connection = get_connection()
cursor = connection.cursor()

cursor.execute(
    """
    SELECT DISTINCT agent_id
    FROM posts
    """
)

agents = cursor.fetchall()

connection.close()

print("Agent IDs found in posts:")

for agent in agents:
    print(agent[0])