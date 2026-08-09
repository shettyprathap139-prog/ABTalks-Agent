import threading
import time

from app.services.news_fetcher import fetch_news
from app.services.editor import rank_articles
from app.services.writer import write_post
from app.services.publisher import publish_post, get_published_urls


active_agents = set()


def run_agent_cycle(agent_id, persona):
    print("\n========== AGENT CYCLE STARTED ==========")

    try:
        # 1. Fetch recent security-relevant news
        articles = fetch_news()

        if not articles:
            print("No articles found.")
            return

        print(f"Found {len(articles)} security-relevant articles.")

        # 2. Remove articles already published
        published_urls = get_published_urls(agent_id)

        new_articles = [
            article
            for article in articles
            if article["url"] not in published_urls
        ]

        print(
            f"New articles available: "
            f"{len(new_articles)} / {len(articles)}"
        )

        if not new_articles:
            print("No new articles available.")
            return

        # 3. Ask AI to rank the new articles
        ranking = rank_articles(new_articles, persona)

        if not ranking.get("ranked_indices"):
            print("AI returned no article ranking.")
            return

        # 4. Try articles in ranking order
        for index in ranking["ranked_indices"]:

            if index < 0 or index >= len(new_articles):
                continue

            article = new_articles[index]

            if article["url"] in published_urls:
                continue

            print("Selected article:", article["title"])

            # 5. Generate the social-media post
            post = write_post(article, persona)

            if not post:
                print("AI did not generate a post.")
                continue

            # 6. Publish the post to SQLite + Breeth memory
            published_post = publish_post(
                agent_id,
                post
            )

            print("New post published:")
            print(published_post)

            return published_post

        print("No suitable unpublished article could be processed.")

    except Exception as error:
        print(f"Agent cycle error: {error}")

    finally:
        print("========== AGENT CYCLE FINISHED ==========\n")


def start_agent(agent_id, persona, interval=300):

    if agent_id in active_agents:
        print(f"Agent {agent_id} is already running.")
        return None

    active_agents.add(agent_id)

    def loop():
        while True:

            try:
                run_agent_cycle(agent_id, persona)

            except Exception as error:
                print(f"Background agent error: {error}")

            print(
                f"Waiting {interval} seconds until next cycle..."
            )

            time.sleep(interval)

    thread = threading.Thread(
        target=loop,
        daemon=True
    )

    thread.start()

    print(
        f"Autonomous agent started for {agent_id}."
    )

    return thread