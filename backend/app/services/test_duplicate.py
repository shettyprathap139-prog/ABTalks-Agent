from app.services.publisher import already_published


agent_id = "9559416f-789c-4c7a-8cb8-e06087b75d2e"

source_url = "https://openai.com/index/responding-next-frontier-critical-cyber-capabilities"

result = already_published(agent_id, source_url)

print("Already published:", result)