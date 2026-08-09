from app.services.news_fetcher import fetch_news
from app.services.editor import choose_article
from app.services.writer import write_post


articles = fetch_news()

persona = {
    "name": "Alex",
    "domain": "AI Security"
}


decision = choose_article(articles, persona)

selected_article = articles[decision["selected_index"]]

post = write_post(selected_article, persona)


print("Generated Post:")
print(post)