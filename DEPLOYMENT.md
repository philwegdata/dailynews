# Deployment Guide

## Option 1: GitHub Actions + GitHub Pages (100% Free)

This is the **recommended** approach - fully automated, no server needed!

### How it works:
1. GitHub Actions runs the aggregation daily at 6 AM CET
2. Results are committed to the repo
3. GitHub Pages serves the static website
4. Everything updates automatically!

### Setup Steps:

#### 1. Create GitHub Repository

```bash
cd "/Users/phil/My Drive/18bresearch/dailynews"

# Initialize git
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/dailynews.git
git push -u origin main
```

#### 2. Add API Key as Secret

1. Go to your GitHub repo
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `GOOGLE_API_KEY`
5. Value: Your Gemini API key
6. Click **Add secret**

#### 3. Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Source: **GitHub Actions**
3. Click **Save**

#### 4. Enable GitHub Actions

1. Go to **Actions** tab
2. If prompted, click **I understand my workflows, go ahead and enable them**

### That's it!

- **Daily aggregation** runs automatically at 6 AM CET
- **Website** available at: `https://YOUR_USERNAME.github.io/dailynews/`
- **Manual trigger**: Go to Actions tab → Daily News Aggregation → Run workflow

---

## Option 2: Cloud Platforms (Always-On Server)

If you want the full FastAPI backend running 24/7:

### A. Render.com (Free Tier)

**Pros:** Easy, free tier, automatic deployments
**Cons:** Spins down after 15 min inactivity

1. Create account at https://render.com
2. Connect your GitHub repo
3. Create **Web Service**:
   - Environment: Python
   - Build: `pip install -r requirements.txt`
   - Start: `python main.py`
4. Add environment variable: `GOOGLE_API_KEY`
5. Deploy!

**URL:** `https://your-app.onrender.com`

### B. Railway.app (Free $5/month credit)

**Pros:** Very easy, great for Python
**Cons:** Limited free tier

1. Go to https://railway.app
2. **New Project** → **Deploy from GitHub**
3. Select your repo
4. Add environment variable: `GOOGLE_API_KEY`
5. Railway auto-detects Python and runs it

**URL:** Auto-generated Railway URL

### C. Fly.io (Free Tier)

**Pros:** Always-on, good performance
**Cons:** Requires CLI setup

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch app
flyctl launch

# Set secret
flyctl secrets set GOOGLE_API_KEY="your_key_here"

# Deploy
flyctl deploy
```

### D. Google Cloud Run (Free Tier)

**Pros:** Scales to zero, cheap
**Cons:** More complex setup

1. Install gcloud CLI
2. Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

3. Deploy:
```bash
gcloud run deploy dailynews \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY="your_key_here"
```

---

## Option 3: Static Site Only (No Backend)

Generate JSON files locally, upload to any static host:

### Setup:

```bash
# Run aggregation locally
python -m backend.aggregator

# Upload these to static host:
# - frontend/
# - data/
```

**Works on:**
- GitHub Pages (free)
- Netlify (free)
- Vercel (free)
- Cloudflare Pages (free)

**Limitation:** No automatic daily updates (must run locally)

---

## Comparison Table

| Solution | Cost | Auto-Updates | Backend | Setup Difficulty |
|----------|------|--------------|---------|-----------------|
| **GitHub Actions + Pages** | Free | ✅ Daily | ❌ | Easy |
| Render.com | Free* | ✅ | ✅ | Very Easy |
| Railway.app | $5/mo | ✅ | ✅ | Very Easy |
| Fly.io | Free* | ✅ | ✅ | Medium |
| Google Cloud Run | Free* | ✅ | ✅ | Hard |
| Static Host (manual) | Free | ❌ | ❌ | Very Easy |

*Free tier with limitations

---

## Recommended: GitHub Actions Setup

For your use case, **GitHub Actions + GitHub Pages is perfect** because:

✅ **100% free** (no credit card needed)
✅ **Automatic daily updates** at 6 AM CET
✅ **No server to maintain**
✅ **Version controlled** (all history in git)
✅ **Easy to update** (just push to repo)
✅ **Public or private** (your choice)

### Quick Start Commands:

```bash
cd "/Users/phil/My Drive/18bresearch/dailynews"

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: AI News Aggregator"

# Create GitHub repo and push
# (Create repo on github.com first)
git remote add origin https://github.com/YOUR_USERNAME/dailynews.git
git push -u origin main

# Add your API key as a GitHub Secret (via web UI)
# Then enable GitHub Pages in Settings → Pages
```

That's it! Your site will be live at `https://YOUR_USERNAME.github.io/dailynews/`

---

## Monitoring Your Deployment

### GitHub Actions:
- Check **Actions** tab to see workflow runs
- View logs if aggregation fails
- Manual trigger: **Run workflow** button

### Check if it's working:
```bash
# Check if daily JSON was created
curl https://YOUR_USERNAME.github.io/dailynews/data/$(date +%Y-%m-%d).json
```

---

## Troubleshooting

**Workflow not running:**
- Check Actions tab is enabled
- Verify cron schedule (UTC time)
- Check secrets are set correctly

**Pages not updating:**
- Check Pages is enabled in Settings
- Verify build/deploy workflow succeeded
- May take 2-5 minutes to propagate

**API quota exceeded:**
- Free tier: 15 requests/min, 1M tokens/day
- Reduce sources or use description fallback
- Upgrade to paid tier if needed

---

## Next Steps After Deployment

1. ✅ Verify daily workflow runs
2. ✅ Check website loads correctly
3. ✅ Test manual workflow trigger
4. ✅ Add custom domain (optional)
5. ✅ Set up monitoring/alerts
6. ✅ Share your news feed with others!

Need help? Check the Actions logs or open an issue on GitHub.
