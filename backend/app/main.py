from fastapi import FastAPI

from app.api.agent import router as agent_router
from app.database.database import initialize_database
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# your existing routers below...
title="ABTalks Autonomous AI Agent",
version="1.0.0"



initialize_database()

app.include_router(agent_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the ABTalks Autonomous AI Agent!"
    }