import httpx
import hashlib
from datetime import datetime, timedelta
from typing import List
from backend.models import Article, Source


class HackerNewsFetcher:
    """Fetches top stories from Hacker News"""

    BASE_URL = "https://hacker-news.firebaseio.com/v0"

    @staticmethod
    async def fetch(source: Source, lookback_hours: int = 24, min_score: int = 50) -> List[Article]:
        """
        Fetch top stories from Hacker News

        Args:
            source: Source configuration
            lookback_hours: How far back to look for content
            min_score: Minimum score for stories to include

        Returns:
            List of Article objects
        """
        articles = []

        try:
            async with httpx.AsyncClient() as client:
                # Get top story IDs
                response = await client.get(f"{HackerNewsFetcher.BASE_URL}/topstories.json")
                story_ids = response.json()[:100]  # Get top 100 stories

                # Calculate cutoff time
                cutoff_timestamp = (datetime.now() - timedelta(hours=lookback_hours)).timestamp()

                # Fetch details for each story
                for story_id in story_ids:
                    try:
                        story_response = await client.get(f"{HackerNewsFetcher.BASE_URL}/item/{story_id}.json")
                        story = story_response.json()

                        # Skip if no URL (Ask HN, Show HN without link, etc.)
                        if not story.get('url'):
                            continue

                        # Skip if too old
                        if story.get('time', 0) < cutoff_timestamp:
                            continue

                        # Skip if score too low
                        if story.get('score', 0) < min_score:
                            continue

                        # Create article
                        article_id = hashlib.md5(f"HN:{story_id}".encode()).hexdigest()
                        published_date = datetime.fromtimestamp(story['time'])

                        article = Article(
                            id=article_id,
                            title=story.get('title', 'Untitled'),
                            source_name=source.name,
                            source_type=source.type,
                            url=story['url'],
                            description=f"HN Score: {story.get('score', 0)} | Comments: {story.get('descendants', 0)}",
                            published_date=published_date
                        )

                        articles.append(article)

                    except Exception as e:
                        print(f"Error fetching HN story {story_id}: {str(e)}")
                        continue

        except Exception as e:
            print(f"Error fetching from Hacker News: {str(e)}")

        return articles
