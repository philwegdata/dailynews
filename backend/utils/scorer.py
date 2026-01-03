import re
from typing import List
from backend.models import Article
from backend.config import KEYWORDS


class RelevanceScorer:
    """Scores articles based on keyword relevance"""

    def __init__(self):
        self.high_priority = KEYWORDS.get('high_priority', [])
        self.medium_priority = KEYWORDS.get('medium_priority', [])
        self.general = KEYWORDS.get('general', [])

    def score_article(self, article: Article) -> float:
        """
        Calculate relevance score for an article

        Args:
            article: Article to score

        Returns:
            Relevance score (higher is more relevant)
        """
        # Combine title and description for scoring
        text = f"{article.title} {article.description or ''}".lower()

        score = 0.0

        # Check high priority keywords (3x weight)
        for keyword in self.high_priority:
            if keyword.lower() in text:
                score += 3.0

        # Check medium priority keywords (2x weight)
        for keyword in self.medium_priority:
            if keyword.lower() in text:
                score += 2.0

        # Check general keywords (1x weight)
        for keyword in self.general:
            if keyword.lower() in text:
                score += 1.0

        return score

    def score_and_rank(self, articles: List[Article], top_n: int = 15) -> List[Article]:
        """
        Score and rank articles, returning top N

        Args:
            articles: List of articles to score
            top_n: Number of top articles to return

        Returns:
            Top N scored and ranked articles
        """
        # Score each article
        for article in articles:
            article.score = self.score_article(article)

        # Sort by score (descending) and published date (recent first)
        ranked_articles = sorted(
            articles,
            key=lambda x: (x.score, x.published_date),
            reverse=True
        )

        return ranked_articles[:top_n]
