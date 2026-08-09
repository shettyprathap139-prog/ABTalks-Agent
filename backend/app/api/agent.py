from app.scheduler.agent_runner import start_agent
from fastapi import APIRouter, Query
from uuid import uuid4
from datetime import datetime, timezone
import json

from app.models.agent import AgentInitRequest
from app.models.post import PostCreate
from app.database.database import get_connection


router = APIRouter(prefix="/api/agent", tags=["Agent"])


@router.post("/init")
def initialize_agent(request: AgentInitRequest):
    agent_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO agents (agent_id, name, domain, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            agent_id,
            request.persona.name,
            request.persona.domain,
            created_at
        )
    )

    connection.commit()
    connection.close()

    persona = {
        "name": request.persona.name,
        "domain": request.persona.domain
    }

    start_agent(agent_id, persona)

    return {
        "agentId": agent_id,
        "status": "initialized"
    }

@router.get("/feed")
def get_feed(agentId: str = Query(...)):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, created_at, text, rationale, sources
        FROM posts
        WHERE agent_id = ?
        ORDER BY created_at DESC
        """,
        (agentId,)
    )

    rows = cursor.fetchall()

    posts = []

    for row in rows:
        posts.append({
            "id": row["id"],
            "createdAt": row["created_at"],
            "text": row["text"],
            "rationale": row["rationale"],
            "sources": json.loads(row["sources"])
        })

    connection.close()

    return {
        "posts": posts
    }


@router.post("/test-post")
def create_test_post(agentId: str, post: PostCreate):
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
            agentId,
            created_at,
            post.text,
            post.rationale,
            json.dumps(post.sources)
        )
    )

    connection.commit()
    connection.close()

    return {
        "id": post_id,
        "createdAt": created_at,
        "text": post.text,
        "rationale": post.rationale,
        "sources": post.sources
    }