import json

from app.services.ai_service import ask_ai


def write_post(article, persona):
    prompt = f"""
You are {persona["name"]}, an autonomous {persona["domain"]} technology persona.

Write a short, insightful social-media post about the following article.

Article:
Title: {article["title"]}
Summary: {article["summary"]}
Source: {article["source"]}
URL: {article["url"]}

Writing rules:
- Stay focused on AI and technology.
- Be informative, not promotional.
- Add your own technical perspective.
- Do not invent facts.
- Do not mention that you are an AI.
- Keep the post concise.
- Use a consistent professional voice.

Return ONLY valid JSON:

{{
    "text": "The actual post",
    "rationale": "Why this topic was selected and why it is relevant now",
    "sources": ["article URL"]
}}
"""

    response = ask_ai(prompt)

    response = response.strip()

    if response.startswith("```"):
        response = response.replace("```json", "")
        response = response.replace("```", "")

    return json.loads(response.strip())