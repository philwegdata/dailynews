from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from datetime import date, timedelta
from typing import List
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager

from backend.aggregator import NewsAggregator
from backend.models import Article
from backend.config import DISPLAY_CONFIG
from backend.scheduler import DailyScheduler


# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: start the scheduler
    scheduler = DailyScheduler()
    scheduler.start()
    app.state.scheduler = scheduler
    yield
    # Shutdown: stop the scheduler
    scheduler.stop()


# Create FastAPI app
app = FastAPI(title="AI News Aggregator", lifespan=lifespan)

# Initialize aggregator
aggregator = NewsAggregator()

# Mount static files
static_dir = Path(__file__).parent.parent.parent / "frontend" / "static"
templates_dir = Path(__file__).parent.parent.parent / "frontend" / "templates"


@app.get("/api/articles/{date_str}")
async def get_articles(date_str: str):
    """
    Get articles for a specific date

    Args:
        date_str: Date in ISO format (YYYY-MM-DD)

    Returns:
        List of articles for that date
    """
    try:
        target_date = date.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    articles = aggregator.load_daily_data(target_date)

    if not articles:
        raise HTTPException(status_code=404, detail=f"No articles found for {date_str}")

    return {
        "date": date_str,
        "articles": [article.model_dump() for article in articles]
    }


@app.get("/api/articles")
async def get_today_articles():
    """Get today's articles (or generate if not yet available)"""
    today = date.today()
    articles = aggregator.load_daily_data(today)

    # If no articles for today, run aggregation
    if not articles:
        print("No articles for today, running aggregation...")
        articles = await aggregator.run_daily_aggregation()

    return {
        "date": today.isoformat(),
        "articles": [article.model_dump() for article in articles]
    }


@app.get("/api/available-dates")
async def get_available_dates():
    """Get all dates with available data"""
    dates = aggregator.get_available_dates()
    return {
        "dates": [d.isoformat() for d in dates]
    }


@app.post("/api/refresh")
async def refresh_today():
    """Manually trigger aggregation for today"""
    articles = await aggregator.run_daily_aggregation()
    return {
        "status": "success",
        "articles_count": len(articles),
        "date": date.today().isoformat()
    }


@app.get("/api/config")
async def get_config():
    """Get display configuration"""
    return DISPLAY_CONFIG


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the main HTML page"""
    html_file = templates_dir / "index.html"

    if not html_file.exists():
        return HTMLResponse(content="<h1>Frontend not yet built. Please create templates/index.html</h1>")

    with open(html_file, 'r') as f:
        content = f.read()

    return HTMLResponse(content=content)


# Mount static files after routes
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
