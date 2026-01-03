import feedparser
import hashlib
from datetime import datetime, timedelta
from typing import List
from backend.models import Article, Source


class RSSFetcher:
    """Fetches articles from RSS feeds (YouTube, podcasts, newsletters)"""

    @staticmethod
    def fetch(source: Source, lookback_hours: int = 48) -> List[Article]:
        """
        Fetch articles from an RSS feed

        Args:
            source: Source configuration
            lookback_hours: How far back to look for content (default 48 hours)

        Returns:
            List of Article objects
        """
        articles = []

        # Determine the RSS URL
        rss_url = source.rss if source.rss else source.url

        try:
            feed = feedparser.parse(rss_url)

            # Calculate cutoff time
            cutoff_time = datetime.now() - timedelta(hours=lookback_hours)

            for entry in feed.entries:
                # Parse published date
                published_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published_date = datetime(*entry.updated_parsed[:6])
                else:
                    # If no date, use current time
                    published_date = datetime.now()

                # Skip if too old
                if published_date < cutoff_time:
                    continue

                # Get URL
                url = entry.link if hasattr(entry, 'link') else source.url

                # Create unique ID
                article_id = hashlib.md5(f"{source.name}:{url}".encode()).hexdigest()

                # Extract description
                description = ""
                if hasattr(entry, 'summary'):
                    description = entry.summary
                elif hasattr(entry, 'description'):
                    description = entry.description

                article = Article(
                    id=article_id,
                    title=entry.title if hasattr(entry, 'title') else "Untitled",
                    source_name=source.name,
                    source_type=source.type,
                    url=url,
                    description=description,
                    published_date=published_date
                )

                articles.append(article)

        except Exception as e:
            print(f"Error fetching from {source.name}: {str(e)}")

        return articles
