# Architecture Overview

## System Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Daily Scheduler                              │
│                    (6:00 AM CET, APScheduler)                       │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         News Aggregator                              │
│                   (Orchestrates entire process)                      │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
         ┌─────────────────┐       ┌─────────────────┐
         │  RSS Fetcher    │       │   API Fetchers  │
         │  ─────────────  │       │  ──────────────  │
         │  • Podcasts     │       │  • Hacker News  │
         │  • YouTube      │       │  • Hugging Face │
         │  • Newsletters  │       │                 │
         └────────┬────────┘       └────────┬────────┘
                  │                         │
                  └──────────┬──────────────┘
                             ▼
                  ┌──────────────────────┐
                  │  Raw Articles List   │
                  │  (100-200 articles)  │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  Relevance Scorer    │
                  │  ─────────────────   │
                  │  • Keyword matching  │
                  │  • Priority weights  │
                  │  • Ranking           │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  Top 15 Articles     │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  AI Summarizer       │
                  │  ───────────────     │
                  │  • Google Gemini     │
                  │  • 2 sentences/50w   │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  JSON Storage        │
                  │  data/YYYY-MM-DD.json│
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  FastAPI Server      │
                  │  GET /api/articles   │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  Frontend (Browser)  │
                  │  • 3x5 grid layout   │
                  │  • Date tabs         │
                  │  • Click to open     │
                  └──────────────────────┘
```

## Data Flow Details

### 1. Fetching Phase
```python
Sources → Fetchers → Raw Articles

Inputs:
- Source configurations from 'plan' file
- RSS URLs, API endpoints
- Lookback period (24-72 hours)

Outputs:
- List[Article] with:
  - id, title, url, description
  - source_name, source_type
  - published_date, fetched_date
```

### 2. Scoring Phase
```python
Raw Articles → Scorer → Scored Articles

Algorithm:
score = Σ(keyword_matches × priority_weight)

Weights:
- High priority keywords: 3.0
- Medium priority keywords: 2.0
- General keywords: 1.0

Example:
"Industrial AI for Manufacturing":
- "Industrial AI" → 3.0 (high)
- "Manufacturing" → 3.0 (high)
- "AI" → 1.0 (general)
- Total score: 7.0
```

### 3. Ranking Phase
```python
Scored Articles → sort(score, date) → Top 15

Sort keys:
1. score (descending)
2. published_date (recent first)

Output: Top 15 articles
```

### 4. Summarization Phase
```python
Top 15 → Gemini API → Articles with summaries

Prompt:
"Summarize in exactly 2 sentences (max 50 words).
Focus on: what happened, why it matters, industrial AI."

Each article gets concise summary
Fallback: Use description if API unavailable
```

### 5. Storage Phase
```python
Processed Articles → JSON File

Format:
{
  "date": "2026-01-03",
  "articles": [
    {
      "id": "abc123",
      "title": "...",
      "summary": "...",
      "score": 7.5,
      ...
    }
  ]
}

Location: data/2026-01-03.json
```

## Component Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│  FastAPI App (main.py)                                      │
│  ├── NewsAggregator                                         │
│  ├── DailyScheduler                                         │
│  └── Static File Server                                     │
└─────────────────────────────────────────────────────────────┘
         │
         ├─► backend/aggregator.py
         │   ├── RSSFetcher
         │   ├── HackerNewsFetcher
         │   ├── HuggingFaceFetcher
         │   ├── RelevanceScorer
         │   └── Summarizer
         │
         ├─► backend/scheduler.py
         │   └── APScheduler
         │
         └─► frontend/
             ├── index.html
             ├── style.css
             └── app.js
```

## External Dependencies

### APIs Used
1. **Google Gemini** (optional)
   - Purpose: AI summarization
   - Rate: 15 RPM free tier
   - Key required: GOOGLE_API_KEY

2. **Hacker News API** (free, no key)
   - Endpoint: hacker-news.firebaseio.com/v0
   - Methods: topstories.json, item/{id}.json

3. **Hugging Face API** (free, no key)
   - Endpoint: huggingface.co/api/daily_papers
   - Returns: Daily trending papers

4. **RSS Feeds** (free, no key)
   - All podcasts, newsletters, YouTube
   - Standard RSS/Atom format

### Python Packages
- fastapi: Web framework
- uvicorn: ASGI server
- feedparser: RSS parsing
- httpx/aiohttp: HTTP clients
- google-generativeai: Gemini SDK
- apscheduler: Cron scheduling
- pydantic: Data validation

## Configuration System

```
plan file (YAML)
    │
    ├─► sources[] → Fetchers
    ├─► keywords{} → Scorer
    ├─► llm{} → Summarizer
    └─► display{} → Frontend

.env file
    └─► GOOGLE_API_KEY → Summarizer
```

## Performance Characteristics

### Timing (estimated)
- Fetching: 5-10 seconds (parallel)
- Scoring: <1 second (100-200 articles)
- Summarizing: 15-30 seconds (15 articles, Gemini)
- Total: ~30-60 seconds per run

### Resource Usage
- Memory: ~100-200 MB
- Disk: ~10 KB per daily JSON file
- Network: ~1-2 MB per aggregation

### Scalability
- Articles per day: 15 (configurable)
- Sources: 10 (easily add more)
- Historical storage: Unlimited (1 JSON file per day)
- Concurrent users: 100+ (FastAPI async)

## Security Considerations

1. **API Keys**: Stored in .env, not committed to git
2. **Input Validation**: Pydantic models validate all data
3. **XSS Prevention**: Frontend escapes all HTML
4. **CORS**: Not configured (localhost only by default)
5. **Rate Limiting**: Not implemented (single user app)

## Extensibility Points

### Add New Source Type
1. Create fetcher in `backend/fetchers/`
2. Add source config to `plan` file
3. Update aggregator to call new fetcher

### Add New Scoring Algorithm
1. Modify `backend/utils/scorer.py`
2. Implement new scoring logic
3. Adjust weights in `plan` file

### Add Authentication
1. Add auth middleware to FastAPI
2. Implement user sessions
3. Multi-user data storage

### Deploy to Cloud
1. Containerize with Docker
2. Deploy to AWS/GCP/Heroku
3. Configure environment variables
4. Set up domain/SSL

## Monitoring & Debugging

### Logs
- Console output during aggregation
- FastAPI access logs
- Scheduler job execution logs

### Data Inspection
```bash
# Check today's data
cat data/$(date +%Y-%m-%d).json | jq

# List all dates
ls -1 data/*.json

# Count articles per day
jq '.articles | length' data/*.json
```

### Manual Testing
```bash
# Test RSS fetching
python test_fetch.py

# Run aggregation once
python -m backend.aggregator

# Test scheduler (runs once immediately)
python -m backend.scheduler
```

## Production Deployment Checklist

- [ ] Set GOOGLE_API_KEY in .env
- [ ] Configure proper logging
- [ ] Set up systemd/launchd service
- [ ] Configure firewall (if public)
- [ ] Set up backup for data/ directory
- [ ] Monitor scheduler execution
- [ ] Set up error notifications
- [ ] Configure reverse proxy (nginx)
- [ ] Enable HTTPS (Let's Encrypt)
- [ ] Optimize Gemini API quota usage

---

**Architecture Principles:**
- Modular: Each component has single responsibility
- Async: Non-blocking I/O for fetching
- Stateless: API server doesn't store session state
- File-based: Simple JSON storage, no database needed
- Resilient: Fallbacks for API failures
