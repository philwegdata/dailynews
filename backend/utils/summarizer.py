import google.generativeai as genai
from typing import List
from backend.models import Article
from backend.config import settings, LLM_CONFIG


class Summarizer:
    """Generates AI summaries for articles using Google Gemini"""

    def __init__(self):
        # Configure Gemini API
        if settings.google_api_key:
            genai.configure(api_key=settings.google_api_key)
            self.model = genai.GenerativeModel(LLM_CONFIG.get('model', 'gemini-1.5-flash'))
            self.enabled = True
        else:
            print("Warning: GOOGLE_API_KEY not set. Summaries will be disabled.")
            self.enabled = False

    def summarize_article(self, article: Article) -> str:
        """
        Generate a summary for a single article

        Args:
            article: Article to summarize

        Returns:
            AI-generated summary (2 sentences, max 50 words)
        """
        if not self.enabled:
            return article.description[:100] + "..." if article.description else ""

        try:
            # Build prompt
            prompt_template = LLM_CONFIG.get('summary_prompt', '')
            prompt = prompt_template.format(
                title=article.title,
                source=article.source_name,
                description=article.description or "No description available"
            )

            # Generate summary
            response = self.model.generate_content(prompt)
            summary = response.text.strip()

            return summary

        except Exception as e:
            print(f"Error generating summary for {article.title}: {str(e)}")
            # Fallback to truncated description
            return article.description[:100] + "..." if article.description else ""

    def summarize_batch(self, articles: List[Article]) -> List[Article]:
        """
        Generate summaries for a batch of articles

        Args:
            articles: List of articles to summarize

        Returns:
            Articles with summaries populated
        """
        for article in articles:
            article.summary = self.summarize_article(article)

        return articles
