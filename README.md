# AI News Aggregator

A modern, minimal web application that automatically aggregates and ranks the most relevant AI and industrial technology news from your trusted sources every day.

## Features

- **Automated Daily Aggregation**: Fetches news every morning at 6 AM CET from multiple sources
- **Smart Relevance Ranking**: Scores articles based on your interests (industrial AI, manufacturing, ML/AI)
- **AI-Powered Summaries**: Uses Google Gemini to generate concise 2-sentence summaries
- **Beautiful 3x5 Tile Grid**: Modern, minimal dark-mode interface
- **Historical Archive**: Browse past days with easy date navigation
- **No API Keys Required** (except Gemini): All sources use free RSS feeds and public APIs

## Supported Sources

### Podcasts (RSS)
- Industrial AI Podcast
- IoT Use Case Podcast
- Doppelgänger Tech Talk
- Manufacturing Happy Hour

### YouTube (RSS)
- Super Data Science

### Newsletters (RSS/Substack)
- Exponential Industry
- The Sequence
- Where's Your Ed At

### News & Research
- Hacker News (Firebase API)
- Hugging Face Daily Papers (API)

## Installation

### 1. Clone and Setup

```bash
cd dailynews
source .venv/bin/activate  # Virtual environment already created
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Get a free Google Gemini API key:
- Visit: https://aistudio.google.com/apikey
- Create API key (free tier: 15 RPM, 1M tokens/day)

Create `.env` file:
```bash
cp .env.example .env
# Edit .env and add your API key
```

## Usage

### Start the Application

```bash
python main.py
```

This will:
1. Start the web server on http://localhost:8000
2. Start the scheduler (daily updates at 6 AM CET)
3. Automatically fetch today's news on first visit

### Manual Commands

**Run aggregation manually:**
```bash
python -m backend.aggregator
```

**Test the scheduler:**
```bash
python -m backend.scheduler
```

### Access the Website

Open your browser and go to:
```
http://localhost:8000
```

## How It Works

1. **Fetching**: Every morning at 6 AM CET (or on-demand), the aggregator:
   - Fetches articles from all RSS feeds
   - Queries Hacker News API for top stories (score > 50)
   - Gets daily papers from Hugging Face

2. **Scoring**: Articles are scored based on keyword relevance:
   - High priority keywords (3x): "industrial AI", "manufacturing AI", "IIoT", etc.
   - Medium priority (2x): "LLM", "machine learning", "MLOps", etc.
   - General keywords (1x): "AI", "neural network", "OpenAI", etc.

3. **Ranking**: Top 15 articles are selected based on:
   - Relevance score
   - Publication recency

4. **Summarization**: Google Gemini generates concise summaries for each article

5. **Storage**: Results are saved to `data/{date}.json` for historical access

## Project Structure

```
dailynews/
├── backend/
│   ├── api/
│   │   └── main.py          # FastAPI application
│   ├── fetchers/
│   │   ├── rss_fetcher.py   # RSS/YouTube/Podcast fetcher
│   │   ├── hacker_news_fetcher.py
│   │   └── huggingface_fetcher.py
│   ├── models/
│   │   └── article.py       # Data models
│   ├── utils/
│   │   ├── scorer.py        # Relevance scoring
│   │   └── summarizer.py    # AI summarization
│   ├── aggregator.py        # Main aggregation logic
│   ├── scheduler.py         # Daily scheduling
│   └── config.py            # Configuration loader
├── frontend/
│   ├── static/
│   │   ├── css/style.css    # Minimal dark theme
│   │   └── js/app.js        # Interactive UI
│   └── templates/
│       └── index.html       # Main page
├── data/                     # Daily JSON files (YYYY-MM-DD.json)
├── plan                      # Original configuration
├── requirements.txt
├── main.py                  # Entry point
└── README.md

```

## Configuration

Edit the `plan` file to customize:

### Sources
Add/remove sources in the `sources:` section. Each source needs:
- `name`: Display name
- `type`: youtube_rss, podcast, newsletter, or api
- `url`: Source URL
- `rss` or `api_endpoint`: Feed/API URL

### Keywords
Modify `keywords:` section to adjust relevance scoring:
- `high_priority`: 3x weight
- `medium_priority`: 2x weight
- `general`: 1x weight

### Display
Change in `display:` section:
- `articles_per_day`: Number of articles to show (default: 15)
- `grid_columns`: Grid width (default: 5)
- `update_time`: Daily fetch time (default: "06:00")
- `timezone`: Timezone for scheduling (default: "Europe/Berlin")

## API Endpoints

- `GET /` - Main web interface
- `GET /api/articles` - Get today's articles (auto-fetches if needed)
- `GET /api/articles/{date}` - Get articles for specific date (YYYY-MM-DD)
- `GET /api/available-dates` - List all dates with data
- `POST /api/refresh` - Manually trigger today's aggregation
- `GET /api/config` - Get display configuration

## Tips

1. **First Run**: On first access, the app will fetch today's news automatically
2. **Daily Updates**: Let it run continuously for automatic daily updates at 6 AM
3. **Historical Data**: All past days are preserved in the `data/` folder
4. **Customization**: Edit the `plan` file and restart to apply changes
5. **No Summaries**: If you don't set `GOOGLE_API_KEY`, it will use article descriptions

## Troubleshooting

**No articles showing:**
- Check that sources are accessible
- Try manual refresh: `POST http://localhost:8000/api/refresh`

**Summaries not working:**
- Verify `GOOGLE_API_KEY` is set in `.env`
- Check API quota at https://aistudio.google.com/

**Scheduler not running:**
- Check timezone configuration in `plan` file
- Verify cron syntax in scheduler logs

## License

MIT

## Credits

Built with:
- FastAPI (web framework)
- Google Gemini (AI summaries)
- feedparser (RSS parsing)
- Hacker News API
- Hugging Face API
