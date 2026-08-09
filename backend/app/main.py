from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from uuid import uuid4
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


DEMO_AGENT_ID = "demo-abtalks-agent"


def setup_and_restore_agent():
    connection = get_connection()
    cursor = connection.cursor()

    # Check whether any agents exist
    cursor.execute("SELECT COUNT(*) AS count FROM agents")
    count = cursor.fetchone()["count"]

    if count == 0:
        # Create permanent demo agent
        created_at = datetime.now(timezone.utc).isoformat()

        cursor.execute(
            """
            INSERT INTO agents (agent_id, name, domain, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                DEMO_AGENT_ID,
                "Alex",
                "AI Security",
                created_at
            )
        )

        # Seed demo posts so judges immediately see content
        demo_posts = [
            (
                "AI security requires protecting not only AI models, but also the infrastructure used to evaluate and deploy them. Secure testing environments, strong isolation, telemetry, and careful access controls are becoming essential as AI systems gain more powerful capabilities.",
                "AI security is increasingly dependent on securing the infrastructure surrounding AI systems, not just the models themselves.",
                [
                    "https://openai.com/index/third-party-cyber-evaluations-involving-openai-models"
                ]
            ),
            (
                "As AI systems become more capable, security teams need to evaluate both model behavior and the environments in which those models are tested. Strong sandboxing, monitoring, access controls, and careful red-team procedures can reduce operational risks during AI security evaluations.",
                "AI red-teaming requires security controls around the evaluation environment as well as the model.",
                [
                    "https://openai.com/index/third-party-cyber-evaluations-involving-openai-models"
                ]
            )
        ]

        for text, rationale, sources in demo_posts:
            cursor.execute(
                """
                INSERT INTO posts
                (id, agent_id, created_at, text, rationale, sources)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(uuid4()),
                    DEMO_AGENT_ID,
                    datetime.now(timezone.utc).isoformat(),
                    text,
                    rationale,
                    json.dumps(sources)
                )
            )

        connection.commit()

        print("==========================================")
        print("DEMO AGENT CREATED")
        print(f"Agent ID: {DEMO_AGENT_ID}")
        print("Demo posts created: 2")
        print("==========================================")

    # Restore the newest existing agent after a restart
    cursor.execute(
        """
        SELECT agent_id, name, domain
        FROM agents
        ORDER BY created_at DESC
        LIMIT 1
        """
    )

    agent = cursor.fetchone()
    connection.close()

    if agent:
        persona = {
            "name": agent["name"],
            "domain": agent["domain"]
        }

        print(
            f"Restoring agent {agent['agent_id']} "
            f"({agent['domain']})"
        )

        start_agent(
            agent["agent_id"],
            persona
        )


initialize_database()
setup_and_restore_agent()

app.include_router(agent_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the ABTalks Autonomous AI Agent!"
    }