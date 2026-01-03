from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Source(BaseModel):
    """Represents a news source"""
    name: str
    type: str  # youtube_rss, podcast, newsletter, api
    url: str
    rss: Optional[str] = None
    api_endpoint: Optional[str] = None
    language: str
    frequency: str
    focus: str
    color: Optional[str] = None


class Article(BaseModel):
    """Represents a news article/content item"""
    id: str
    title: str
    source_name: str
    source_type: str
    url: str
    description: Optional[str] = None
    summary: Optional[str] = None  # AI-generated summary
    published_date: datetime
    fetched_date: datetime = Field(default_factory=datetime.now)
    score: float = 0.0  # Relevance score

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
