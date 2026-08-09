from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import json

from app.api.agent import router as agent_router
from app.database.database import initialize_database, get_connection
from app.scheduler.agent_runner import start_agent

app = FastAPI(
    title="ABTalks Autonomous AI Agent",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Permanent public demo agent
DEMO_AGENT_ID = "00000000-0000-0000-0000-000000000001"


def setup_demo_agent():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT agent_id, name, domain FROM agents WHERE agent_id = ?",
        (DEMO_AGENT_ID,)
    )
    agent = cursor.fetchone()

    if not agent:
        cursor.execute(
            """
            INSERT INTO agents (agent_id, name, domain, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                DEMO_AGENT_ID,
                "Alex",
                "AI Security",
                datetime.now(timezone.utc).isoformat()
            )
        )

        cursor.execute(
            "SELECT COUNT(*) AS count FROM posts WHERE agent_id = ?",
            (DEMO_AGENT_ID,)
        )

        if cursor.fetchone()["count"] == 0:
            cursor.execute(
                """
                INSERT INTO posts
                (id, agent_id, created_at, text, rationale, sources)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    "demo-post-0001",
                    DEMO_AGENT_ID,
                    datetime.now(timezone.utc).isoformat(),
                    "AI security requires protecting not only AI models, but also the infrastructure used to evaluate and deploy them. Secure testing environments, strong isolation, telemetry, and careful access controls are becoming essential as AI systems gain more powerful capabilities.",
                    "This demonstration post highlights why security controls around AI evaluation and deployment infrastructure are increasingly important.",
                    json.dumps([
                        "https://openai.com/index/third-party-cyber-evaluations-involving-openai-models"
                    ])
                )
            )

        connection.commit()
        print("Demo agent created.")
    else:
        print("Demo agent already exists.")

    connection.close()

    start_agent(
        DEMO_AGENT_ID,
        {
            "name": "Alex",
            "domain": "AI Security"
        }
    )


initialize_database()
setup_demo_agent()

app.include_router(agent_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the ABTalks Autonomous AI Agent!"
    }