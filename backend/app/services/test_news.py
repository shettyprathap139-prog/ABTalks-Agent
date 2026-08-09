from news_fetcher import fetch_news


articles = fetch_news()

print(f"Found {len(articles)} articles")

for article in articles[:5]:
    print("\n---")
    print(article["title"])
    print(article["source"])
    print(article["url"])