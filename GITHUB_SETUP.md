# GitHub Setup Guide - 5 Minute Deployment

## What You'll Get

✅ Website auto-updates every day at 6 AM CET
✅ Hosted for free on GitHub Pages
✅ No server needed - 100% automated
✅ Public URL: `https://YOUR_USERNAME.github.io/dailynews/`

---

## Step-by-Step Setup

### 1. Prepare Your Repository

```bash
cd "/Users/phil/My Drive/18bresearch/dailynews"

# Initialize git
git init
git add .
git commit -m "Initial commit: AI News Aggregator"
```

### 2. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `dailynews` (or any name you like)
3. Make it **Public** (required for free GitHub Pages)
4. **Do NOT** initialize with README, .gitignore, or license
5. Click **Create repository**

### 3. Push Your Code

Copy the commands from GitHub and run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/dailynews.git
git branch -M main
git push -u origin main
```

### 4. Add Your API Key as Secret

1. Go to your repository on GitHub
2. Click **Settings** tab
3. In left sidebar: **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Name: `GOOGLE_API_KEY`
6. Value: (paste your Gemini API key)
7. Click **Add secret**

### 5. Enable GitHub Pages

1. Still in **Settings**
2. In left sidebar: **Pages**
3. Under "Build and deployment":
   - Source: **GitHub Actions**
4. Click **Save**

### 6. Enable Workflows

1. Click the **Actions** tab
2. If you see "Workflows aren't being run on this forked repository"
   - Click **I understand my workflows, go ahead and enable them**

---

## That's It! 🎉

Your news aggregator is now live!

### What Happens Next:

1. **Daily Aggregation** runs automatically at 6 AM CET (check Actions tab)
2. **GitHub Pages** deploys automatically when new data is added
3. **Website** is live at: `https://YOUR_USERNAME.github.io/dailynews/`

### First Run (Manual)

To get your first data immediately:

1. Go to **Actions** tab
2. Click **Daily News Aggregation**
3. Click **Run workflow** → **Run workflow**
4. Wait ~1-2 minutes for it to complete
5. Your site will auto-deploy!

---

## Checking Your Deployment

### View Workflow Runs
- **Actions** tab → **Daily News Aggregation**
- See logs, errors, and run history

### Visit Your Site
- After first successful run: `https://YOUR_USERNAME.github.io/dailynews/`
- May take 2-5 minutes for first deployment

### Check Data Files
- Browse to: `https://github.com/YOUR_USERNAME/dailynews/tree/main/data`
- Should see files like `2026-01-03.json`

---

## Customization After Deployment

### Change Schedule

Edit `.github/workflows/daily-aggregation.yml`:

```yaml
schedule:
  - cron: '0 4 * * *'  # 4 AM UTC = 6 AM CEST
```

[Cron schedule syntax](https://crontab.guru/)

### Add/Remove Sources

Edit `plan` file, push changes:

```bash
# After editing plan file
git add plan
git commit -m "Update sources"
git push
```

### Manual Refresh

1. Go to **Actions** tab
2. **Daily News Aggregation** → **Run workflow**

---

## Troubleshooting

### "Workflow not running"

**Check:**
- Actions are enabled (Actions tab)
- Secrets are set correctly (Settings → Secrets)
- Workflow file is in `.github/workflows/`

**Fix:**
- Run workflow manually first
- Check for errors in Actions logs

### "Pages not deploying"

**Check:**
- GitHub Pages is enabled (Settings → Pages)
- Source is set to "GitHub Actions"
- Repository is public

**Fix:**
- Wait 5 minutes (can be slow first time)
- Check Actions tab for deployment errors

### "No articles showing"

**Check:**
- At least one workflow has run successfully
- `data/` folder has JSON files
- Check browser console for errors

**Fix:**
- Run workflow manually
- Check if JSON files exist in repo

### "API quota exceeded"

**Symptoms:**
- Workflow fails
- Articles missing summaries

**Fix:**
- Check Gemini API quota at https://aistudio.google.com
- Free tier: 15 RPM, 1M tokens/day
- Reduce number of sources or upgrade

---

## Advanced: Custom Domain

### Add Your Own Domain

1. Buy domain (e.g., `mynews.com`)
2. In DNS settings, add CNAME:
   ```
   www.mynews.com → YOUR_USERNAME.github.io
   ```
3. In GitHub:
   - **Settings** → **Pages**
   - Custom domain: `www.mynews.com`
   - **Enforce HTTPS** ✓

---

## Monitoring

### Daily Workflow Status

Enable email notifications:
1. GitHub profile → **Settings**
2. **Notifications** → **Actions**
3. Check "Email" for workflow failures

### Manual Checks

```bash
# Check if today's data exists
curl https://YOUR_USERNAME.github.io/dailynews/data/$(date +%Y-%m-%d).json

# View latest data
curl https://YOUR_USERNAME.github.io/dailynews/data/$(date +%Y-%m-%d).json | jq
```

---

## Cost Breakdown

| Item | Cost |
|------|------|
| GitHub Repository | **Free** |
| GitHub Actions | **Free** (2,000 min/month) |
| GitHub Pages | **Free** (100 GB bandwidth/month) |
| Google Gemini API | **Free** (1M tokens/day) |
| **Total** | **$0/month** |

Your news aggregator costs **absolutely nothing** to run! 🎉

---

## What Happens Daily

**Every day at 6:00 AM CET:**

1. ⏰ GitHub Actions triggers workflow
2. 📡 Fetches articles from 10 sources
3. 🎯 Scores & ranks by relevance
4. 🤖 Generates AI summaries with Gemini
5. 💾 Saves to `data/YYYY-MM-DD.json`
6. 📤 Commits and pushes to repo
7. 🚀 GitHub Pages auto-deploys
8. ✅ Your site updates automatically!

All while you sleep! ☕

---

## Support

- **Issues:** Open an issue on GitHub
- **Logs:** Check Actions tab for detailed logs
- **Gemini API:** https://aistudio.google.com
- **GitHub Pages Docs:** https://docs.github.com/pages

---

## Summary Commands

```bash
# Initial setup
cd "/Users/phil/My Drive/18bresearch/dailynews"
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/dailynews.git
git push -u origin main

# Then on GitHub:
# 1. Add GOOGLE_API_KEY secret
# 2. Enable GitHub Pages (Actions)
# 3. Run workflow manually (first time)

# Your site: https://YOUR_USERNAME.github.io/dailynews/
```

**Setup time:** ~5 minutes
**Ongoing maintenance:** None - fully automated!

Enjoy your automated AI news feed! 🚀
