from app.services.news_fetcher import fetch_news
from app.services.editor import rank_articles


articles = fetch_news()

persona = {
    "name": "Alex",
    "domain": "AI Security"
}

result = rank_articles(articles, persona)

print("AI Ranking:")
print(result)

print("\nTop article:")

top_index = result["ranked_indices"][0]

print(articles[top_index])