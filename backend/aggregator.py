import asyncio
import logging
from datetime import datetime, date
from typing import List, Dict
from pathlib import Path
from urllib.parse import urlparse
import json

from backend.models import Article, Source
from backend.fetchers import RSSFetcher, HackerNewsFetcher, HuggingFaceFetcher
from backend.utils import RelevanceScorer, Summarizer
from backend.config import SOURCES, DISPLAY_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class NewsAggregator:
    """Main aggregator that fetches, scores, and ranks news from all sources"""

    def __init__(self):
        self.scorer = RelevanceScorer()
        self.summarizer = Summarizer()
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)

    def deduplicate_articles(self, articles: List[Article]) -> List[Article]:
        """
        Remove duplicate articles based on URL

        Args:
            articles: List of articles that may contain duplicates

        Returns:
            List of unique articles (keeps first occurrence, higher-scored preferred)
        """
        seen_urls: Dict[str, Article] = {}

        for article in articles:
            # Normalize URL for comparison (remove trailing slashes, fragments)
            parsed = urlparse(article.url)
            normalized_url = f"{parsed.netloc}{parsed.path.rstrip('/')}"

            if normalized_url not in seen_urls:
                seen_urls[normalized_url] = article

        unique_articles = list(seen_urls.values())
        logger.info(f"Deduplication: {len(articles)} -> {len(unique_articles)} articles")
        return unique_articles

    async def fetch_all_sources(self) -> List[Article]:
        """
        Fetch articles from all configured sources

        Returns:
            List of all fetched articles
        """
        all_articles = []
        failed_sources = []
        successful_sources = 0

        for source_config in SOURCES:
            source = Source(**source_config)
            logger.info(f"Fetching from {source.name}...")

            try:
                articles = []
                if source.type in ['youtube_rss', 'podcast', 'newsletter']:
                    # Use RSS fetcher
                    articles = RSSFetcher.fetch(source)

                elif source.type == 'api':
                    if 'hacker-news' in source.url:
                        # Use Hacker News fetcher
                        articles = await HackerNewsFetcher.fetch(source)
                    elif 'huggingface' in source.url:
                        # Use Hugging Face fetcher
                        articles = await HuggingFaceFetcher.fetch(source)

                all_articles.extend(articles)
                successful_sources += 1
                logger.info(f"  -> Fetched {len(articles)} articles from {source.name}")

            except Exception as e:
                logger.error(f"Error fetching from {source.name}: {str(e)}")
                failed_sources.append(source.name)

        # Log summary
        logger.info(f"Fetch complete: {successful_sources}/{len(SOURCES)} sources successful")
        if failed_sources:
            logger.warning(f"Failed sources: {', '.join(failed_sources)}")

        logger.info(f"Total articles fetched: {len(all_articles)}")
        return all_articles

    def process_articles(self, articles: List[Article]) -> List[Article]:
        """
        Score, rank, and summarize articles

        Args:
            articles: Raw articles

        Returns:
            Top N processed articles
        """
        # Deduplicate first
        unique_articles = self.deduplicate_articles(articles)

        # Score and rank
        top_n = DISPLAY_CONFIG.get('articles_per_day', 15)
        top_articles = self.scorer.score_and_rank(unique_articles, top_n=top_n)

        logger.info(f"Selected top {len(top_articles)} articles by relevance score")

        # Generate summaries
        logger.info("Generating AI summaries...")
        top_articles = self.summarizer.summarize_batch(top_articles)
        logger.info("Summaries complete")

        return top_articles

    def save_daily_data(self, articles: List[Article], target_date: date = None):
        """
        Save articles to daily JSON file

        Args:
            articles: Articles to save
            target_date: Date to save for (defaults to today)
        """
        if target_date is None:
            target_date = date.today()

        filename = f"{target_date.isoformat()}.json"
        filepath = self.data_dir / filename

        # Convert to JSON
        data = {
            'date': target_date.isoformat(),
            'articles': [article.model_dump() for article in articles]
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        logger.info(f"Saved {len(articles)} articles to {filepath}")

    def load_daily_data(self, target_date: date) -> List[Article]:
        """
        Load articles from a specific date

        Args:
            target_date: Date to load

        Returns:
            List of articles for that date (empty if not found)
        """
        filename = f"{target_date.isoformat()}.json"
        filepath = self.data_dir / filename

        if not filepath.exists():
            return []

        with open(filepath, 'r') as f:
            data = json.load(f)

        articles = [Article(**article_data) for article_data in data['articles']]
        return articles

    def get_available_dates(self) -> List[date]:
        """
        Get all dates with available data

        Returns:
            List of dates (sorted, most recent first)
        """
        dates = []
        for filepath in self.data_dir.glob("*.json"):
            try:
                date_str = filepath.stem
                article_date = date.fromisoformat(date_str)
                dates.append(article_date)
            except ValueError:
                continue

        return sorted(dates, reverse=True)

    async def run_daily_aggregation(self):
        """Run the full daily aggregation process"""
        logger.info("=" * 50)
        logger.info(f"Starting daily aggregation at {datetime.now()}")
        logger.info("=" * 50)

        try:
            # Fetch from all sources
            articles = await self.fetch_all_sources()

            if not articles:
                logger.error("No articles fetched from any source!")
                return []

            # Process articles
            top_articles = self.process_articles(articles)

            # Save to daily file
            self.save_daily_data(top_articles)

            logger.info("=" * 50)
            logger.info(f"Daily aggregation complete! Processed {len(top_articles)} articles")
            logger.info("=" * 50)
            return top_articles

        except Exception as e:
            logger.error(f"Critical error during aggregation: {str(e)}")
            raise


# Entry point for manual execution
async def main():
    aggregator = NewsAggregator()
    await aggregator.run_daily_aggregation()


if __name__ == "__main__":
    asyncio.run(main())
