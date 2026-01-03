# Quick Start Guide

## Step 1: Get Google Gemini API Key (Optional but Recommended)

1. Go to https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy the key

## Step 2: Configure Environment

```bash
# Create .env file
cp .env.example .env

# Edit .env and paste your API key
# If you skip this, the app will work but use article descriptions instead of AI summaries
```

## Step 3: Start the Application

```bash
# Make sure you're in the dailynews directory
cd "/Users/phil/My Drive/18bresearch/dailynews"

# Activate virtual environment
source .venv/bin/activate

# Start the server
python main.py
```

The server will start on http://localhost:8000

## Step 4: Access the Website

Open your browser and go to:
```
http://localhost:8000
```

On first access, it will automatically fetch today's news (this may take 1-2 minutes).

## What Happens Next

- The app fetches articles from all configured sources
- Scores them based on relevance to AI/industrial technology
- Generates AI summaries (if API key is configured)
- Displays top 15 in a beautiful 3x5 grid
- Updates automatically every day at 6:00 AM CET

## Manual Operations

**Force refresh today's news:**
```bash
# While the server is running, in a new terminal:
curl -X POST http://localhost:8000/api/refresh
```

**Run aggregation once (without server):**
```bash
python -m backend.aggregator
```

## Troubleshooting

**ImportError or module not found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**No articles showing:**
- Check your internet connection
- Sources may be temporarily unavailable
- Try manual refresh

**Protobuf errors:**
```bash
# Install compatible protobuf version
pip install 'protobuf>=5.28.0,<6.0.0'
```

## Next Steps

- Customize sources in the `plan` file
- Adjust keywords for better relevance scoring
- Set up as a system service for 24/7 operation
- Add more sources (any RSS feed works!)

Enjoy your personalized AI news feed!
