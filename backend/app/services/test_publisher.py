from app.services.news_fetcher import fetch_news
from app.services.editor import rank_articles
from app.services.writer import write_post
from app.services.publisher import publish_post, already_published


articles = fetch_news()

persona = {
    "name": "Alex",
    "domain": "AI Security"
}

agent_id = "9559416f-789c-4c7a-8cb8-e06087b75d2e"

ranking = rank_articles(articles, persona)

published = False

for index in ranking["ranked_indices"]:
    article = articles[index]

    if already_published(agent_id, article["url"]):
        print(f"Skipping already published article: {article['title']}")
        continue

    print(f"Selected article: {article['title']}")

    post = write_post(article, persona)

    saved_post = publish_post(agent_id, post)

    print("New post published:")
    print(saved_post)

    published = True
    break


if not published:
    print("No new suitable article found.")