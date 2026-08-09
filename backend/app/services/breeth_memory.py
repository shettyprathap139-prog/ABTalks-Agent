import os
import requests
from dotenv import load_dotenv


load_dotenv()

BREETH_API_KEY = os.getenv("BREETH_API_KEY")
BREETH_TEAM_ID = os.getenv("BREETH_TEAM_ID")
BREETH_BASE_URL = "https://api.thebreeth.com/v1"


def save_memory(messages):
    response = requests.post(
        f"{BREETH_BASE_URL}/episodes",
       headers={
    "Authorization": f"Bearer {BREETH_API_KEY.strip()}",
    "X-Cogram-Team-Id": BREETH_TEAM_ID,
    "Content-Type": "application/json"
},
        json={
            "content": "\n".join(
                f"{message['role']}: {message['content']}"
                for message in messages
            )
        },
        timeout=30
    )

    print("Breeth status:", response.status_code)
    print("Breeth response:", response.text)

    response.raise_for_status()
    return response.json()


def search_memory(query, limit=5):
    response = requests.post(
        f"{BREETH_BASE_URL}/search",
        headers={
            "Authorization": f"Bearer {BREETH_API_KEY.strip()}",
            "Content-Type": "application/json"
        },
        json={
            "query": query,
            "limit": limit
        },
        timeout=30
    )

    print("Breeth search status:", response.status_code)
    print("Breeth search response:", response.text)

    response.raise_for_status()
    return response.json()


def record_fact(subject, predicate, object_value):
    response = requests.post(
        f"{BREETH_BASE_URL}/facts",
        headers={
            "Authorization": f"Bearer {BREETH_API_KEY.strip()}",
            "Content-Type": "application/json"
        },
        json={
            "subject": subject,
            "predicate": predicate,
            "object": object_value,
            "group_id": "default"
        },
        timeout=30
    )

    print("Breeth fact status:", response.status_code)
    print("Breeth fact response:", response.text)

    response.raise_for_status()
    return response.json()