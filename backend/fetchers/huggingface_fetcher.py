import httpx
import hashlib
from datetime import datetime
from typing import List
from backend.models import Article, Source


class HuggingFaceFetcher:
    """Fetches daily papers from Hugging Face"""

    @staticmethod
    async def fetch(source: Source) -> List[Article]:
        """
        Fetch daily papers from Hugging Face

        Args:
            source: Source configuration

        Returns:
            List of Article objects
        """
        articles = []

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(source.api_endpoint, timeout=30.0)
                papers = response.json()

                for paper in papers:
                    # Create unique ID
                    paper_id = paper.get('id', paper.get('paper_id', ''))
                    article_id = hashlib.md5(f"HF:{paper_id}".encode()).hexdigest()

                    # Get paper URL
                    url = f"https://huggingface.co/papers/{paper_id}"

                    # Extract title and abstract
                    title = paper.get('title', 'Untitled Paper')
                    abstract = paper.get('abstract', '')

                    # Use upvotes as a simple metric
                    upvotes = paper.get('upvotes', 0)
                    description = f"Upvotes: {upvotes}"
                    if abstract:
                        description += f" | {abstract[:200]}..."

                    article = Article(
                        id=article_id,
                        title=title,
                        source_name=source.name,
                        source_type=source.type,
                        url=url,
                        description=description,
                        published_date=datetime.now()  # HF daily papers are from today
                    )

                    articles.append(article)

        except Exception as e:
            print(f"Error fetching from Hugging Face: {str(e)}")

        return articles
