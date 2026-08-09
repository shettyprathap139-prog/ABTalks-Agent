from app.scheduler.agent_runner import run_agent_cycle


agent_id = "9559416f-789c-4c7a-8cb8-e06087b75d2e"

persona = {
    "name": "Alex",
    "domain": "AI Security"
}


run_agent_cycle(agent_id, persona)