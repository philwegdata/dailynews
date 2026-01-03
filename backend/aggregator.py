import asyncio
from datetime import datetime, date
from typing import List
from pathlib import Path
import json

from backend.models import Article, Source
from backend.fetchers import RSSFetcher, HackerNewsFetcher, HuggingFaceFetcher
from backend.utils import RelevanceScorer, Summarizer
from backend.config import SOURCES, DISPLAY_CONFIG


class NewsAggregator:
    """Main aggregator that fetches, scores, and ranks news from all sources"""

    def __init__(self):
        self.scorer = RelevanceScorer()
        self.summarizer = Summarizer()
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)

    async def fetch_all_sources(self) -> List[Article]:
        """
        Fetch articles from all configured sources

        Returns:
            List of all fetched articles
        """
        all_articles = []

        for source_config in SOURCES:
            source = Source(**source_config)
            print(f"Fetching from {source.name}...")

            try:
                if source.type in ['youtube_rss', 'podcast', 'newsletter']:
                    # Use RSS fetcher
                    articles = RSSFetcher.fetch(source)
                    all_articles.extend(articles)

                elif source.type == 'api':
                    if 'hacker-news' in source.url:
                        # Use Hacker News fetcher
                        articles = await HackerNewsFetcher.fetch(source)
                        all_articles.extend(articles)
                    elif 'huggingface' in source.url:
                        # Use Hugging Face fetcher
                        articles = await HuggingFaceFetcher.fetch(source)
                        all_articles.extend(articles)

            except Exception as e:
                print(f"Error fetching from {source.name}: {str(e)}")

        print(f"Fetched {len(all_articles)} total articles")
        return all_articles

    def process_articles(self, articles: List[Article]) -> List[Article]:
        """
        Score, rank, and summarize articles

        Args:
            articles: Raw articles

        Returns:
            Top N processed articles
        """
        # Score and rank
        top_n = DISPLAY_CONFIG.get('articles_per_day', 15)
        top_articles = self.scorer.score_and_rank(articles, top_n=top_n)

        print(f"Selected top {len(top_articles)} articles")

        # Generate summaries
        top_articles = self.summarizer.summarize_batch(top_articles)

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

        print(f"Saved {len(articles)} articles to {filepath}")

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
        print(f"Starting daily aggregation at {datetime.now()}")

        # Fetch from all sources
        articles = await self.fetch_all_sources()

        # Process articles
        top_articles = self.process_articles(articles)

        # Save to daily file
        self.save_daily_data(top_articles)

        print(f"Daily aggregation complete! Processed {len(top_articles)} articles")
        return top_articles


# Entry point for manual execution
async def main():
    aggregator = NewsAggregator()
    await aggregator.run_daily_aggregation()


if __name__ == "__main__":
    asyncio.run(main())
