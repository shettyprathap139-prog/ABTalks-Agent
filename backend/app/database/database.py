import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "agent.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            agent_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            domain TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            agent_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            text TEXT NOT NULL,
            rationale TEXT NOT NULL,
            sources TEXT NOT NULL,
            FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
        )
    """)

    connection.commit()
    connection.close()