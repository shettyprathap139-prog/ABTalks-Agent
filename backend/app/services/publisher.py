import json
from uuid import uuid4
from datetime import datetime, timezone
from app.services.breeth_memory import save_memory

from app.database.database import get_connection
def already_published(agent_id, source_url):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM posts
        WHERE agent_id = ?
        AND sources LIKE ?
        LIMIT 1
        """,
        (
            agent_id,
            f"%{source_url}%"
        )
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None
def get_published_urls(agent_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT sources
        FROM posts
        WHERE agent_id = ?
        """,
        (agent_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    published_urls = set()

    for row in rows:
        try:
            sources = json.loads(row["sources"])

            for url in sources:
                published_urls.add(url)

        except (json.JSONDecodeError, TypeError):
            continue

    return published_urls

def publish_post(agent_id, post):
    post_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO posts
        (id, agent_id, created_at, text, rationale, sources)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            post_id,
            agent_id,
            created_at,
            post["text"],
            post["rationale"],
            json.dumps(post["sources"])
        )
    )

    connection.commit()
    connection.close()
    try:
        save_memory([
            {
                "role": "user",
                "content": f"Alex published a post about: {post['text']}"
            },
            {
                "role": "assistant",
                "content": f"The published post used source: {post['sources'][0]}"
            }
        ])

        print("Breeth memory saved.")

    except Exception as error:
        print("Breeth memory error:", error)

    return {
        "id": post_id,
        "createdAt": created_at,
        "text": post["text"],
        "rationale": post["rationale"],
        "sources": post["sources"]
    }