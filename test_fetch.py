#!/usr/bin/env python3
"""
Simple test script to verify fetching works
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from backend.models import Source
from backend.fetchers import RSSFetcher

def test_rss_fetch():
    """Test RSS fetching with Hacker News RSS"""
    print("Testing RSS Fetcher...")
    print("=" * 60)

    # Create a test source (using a well-known RSS feed)
    test_source = Source(
        name="Test RSS Feed",
        type="newsletter",
        url="https://news.ycombinator.com/rss",
        rss="https://news.ycombinator.com/rss",
        language="en",
        frequency="continuous",
        focus="Tech news"
    )

    print(f"Fetching from: {test_source.name}")
    articles = RSSFetcher.fetch(test_source, lookback_hours=72)

    print(f"\nFetched {len(articles)} articles")
    print("=" * 60)

    if articles:
        print("\nFirst 3 articles:")
        for i, article in enumerate(articles[:3], 1):
            print(f"\n{i}. {article.title}")
            print(f"   URL: {article.url}")
            print(f"   Published: {article.published_date}")
            if article.description:
                desc = article.description[:100] + "..." if len(article.description) > 100 else article.description
                print(f"   Description: {desc}")
    else:
        print("No articles fetched. This might be normal if no recent content is available.")

    print("\n" + "=" * 60)
    print("✓ RSS Fetcher test complete!")
    return len(articles) > 0

if __name__ == "__main__":
    success = test_rss_fetch()
    sys.exit(0 if success else 1)
