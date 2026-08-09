from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


def restore_latest_agent():
    connection = get_connection()
    cursor = connection.cursor()

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

    if not agent:
        print("No existing agents to restore.")
        return

    agent_id = agent["agent_id"]

    persona = {
        "name": agent["name"],
        "domain": agent["domain"]
    }

    print(
        f"Restoring latest agent: {agent_id} "
        f"({persona['domain']})"
    )

    start_agent(agent_id, persona)


initialize_database()
restore_latest_agent()

app.include_router(agent_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the ABTalks Autonomous AI Agent!"
    }