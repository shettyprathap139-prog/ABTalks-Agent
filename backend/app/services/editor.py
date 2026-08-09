import json

from app.services.ai_service import ask_ai


def rank_articles(articles, persona):
    articles_text = ""

    for index, article in enumerate(articles):
        articles_text += f"""
ARTICLE {index}
Title: {article["title"]}
Source: {article["source"]}
Summary: {article["summary"]}
URL: {article["url"]}
"""

    prompt = f"""
You are the editorial decision-maker for an autonomous AI agent.

Persona:
Name: {persona["name"]}
Domain: {persona["domain"]}

Rank the articles from MOST valuable to LEAST valuable for this persona.

A recent, significant development should normally rank above
an old or historical article, even if the old article is technically relevant.


Ignore:
- advertisements
- duplicate stories
- irrelevant topics
- low-quality content
Consider:
- Importance to the technology community
- Relevance to the persona
- Technical significance
- How recent the development is
- Potential value to readers
- Whether the story represents a meaningful new development

Strongly prefer recent developments.

Avoid:
- Old articles
- Historical projects
- Articles that are several years old
- Stories that are only loosely related to current AI/security developments
- Minor updates with little practical significance
Return ONLY valid JSON:

{{
    "ranked_indices": [0, 4, 2, 7],
    "reasons": {{
        "0": "Why article 0 is valuable",
        "4": "Why article 4 is valuable"
    }}
}}

Articles:
{articles_text}
"""

    response = ask_ai(prompt)

    response = response.strip()

    if response.startswith("```"):
        response = response.replace("```json", "")
        response = response.replace("```", "")

    return json.loads(response.strip())