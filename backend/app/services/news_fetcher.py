import feedparser
from datetime import datetime, timezone, timedelta


RSS_FEEDS = {
    "OpenAI": "https://openai.com/news/rss.xml",
    "Google AI": "https://blog.google/technology/ai/rss/",
    "Hacker News": "https://hnrss.org/frontpage"
}

SECURITY_KEYWORDS = [
    "security",
    "cyber",
    "cybersecurity",
    "vulnerability",
    "vulnerabilities",
    "exploit",
    "exploitation",
    "malware",
    "ransomware",
    "attack",
    "attacks",
    "threat",
    "red team",
    "red-teaming",
    "adversarial",
    "backdoor",
    "breach",
    "phishing",
    "zero-day",
    "zero day",
    "prompt injection",
    "jailbreak",
    "model security",
    "ai security",
    "ai safety",
    "security research",
    "cyber risk",
    "cyber attack",
    "data theft",
    "data breach",
    "safeguard"
]

def looks_security_relevant(article):
    title = article.get("title", "").lower()
    if "cyber" in title:
     return True
    summary = article.get("summary", "").lower()

    strong_security_keywords = [
        "cybersecurity",
        "cyber security",
        "cyber attack",
        "cyberattack",
        "cyber threat",
        "cyber risk",
        "vulnerability",
        "vulnerabilities",
        "exploit",
        "exploitation",
        "malware",
        "ransomware",
        "phishing",
        "zero-day",
        "zero day",
        "prompt injection",
        "jailbreak",
        "adversarial attack",
        "adversarial",
        "red team",
        "red-teaming",
        "backdoor",
        "data breach",
        "security breach",
        "data theft",
        "attack surface"
    ]

    # Strong security signal directly in the title
    if any(keyword in title for keyword in strong_security_keywords):
        return True

    # Otherwise require at least TWO strong security signals
    # in the article summary.
    matches = sum(
        keyword in summary
        for keyword in strong_security_keywords
    )

    return matches >= 2
def fetch_news():
    articles = []

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)

    for source, url in RSS_FEEDS.items():

        try:
            feed = feedparser.parse(url)

            for entry in feed.entries[:10]:

                published_at = None

                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published_at = datetime(
                        *entry.published_parsed[:6],
                        tzinfo=timezone.utc
                    )

                elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                    published_at = datetime(
                        *entry.updated_parsed[:6],
                        tzinfo=timezone.utc
                    )

                # Skip articles older than 30 days
                if published_at and published_at < cutoff_date:
                    continue

                article = {
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "url": entry.get("link", ""),
                    "source": source,
                    "published_at": (
                        published_at.isoformat()
                        if published_at
                        else None
                    )
                }

                # Keep only security-relevant articles
                if looks_security_relevant(article):
                    articles.append(article)

        except Exception as error:
            print(f"News fetch error from {source}: {error}")

    return articles