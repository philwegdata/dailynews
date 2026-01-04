# Troubleshooting Guide

## Current Issues and Fixes

### Issue 1: Only Hugging Face articles showing

**Cause:** RSS fetchers and Hacker News fetcher may be failing silently

**Solution:** Check the GitHub Actions logs to see specific errors

**To debug:**
1. Go to Actions tab → Latest run
2. Click on "Run aggregation" step
3. Look for error messages from specific sources

**Common causes:**
- RSS feeds timing out
- Network issues in GitHub Actions
- Invalid RSS URLs

### Issue 2: No summaries generated

**Cause:** Google Gemini API key may not be set correctly

**Fix:**
1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Check if `GOOGLE_API_KEY` exists
3. If not, add it:
   - Click **New repository secret**
   - Name: `GOOGLE_API_KEY`
   - Value: Your Gemini API key (from .env file)
   - Click **Add secret**

**Verify it worked:**
- Re-run the workflow
- Check the generated JSON file for `"summary"` fields

### Issue 3: Website not deploying to GitHub Pages

**Cause:** GitHub Pages might not be enabled or configured correctly

**Fix:**
1. Go to **Settings** → **Pages**
2. Under "Build and deployment":
   - Source: **GitHub Actions** (not "Deploy from a branch")
3. Click **Save**

**Verify:**
- After pushing, check **Actions** tab
- You should see two workflows:
  1. "Daily News Aggregation"
  2. "Deploy to GitHub Pages"
- Both should complete successfully

**Your site will be at:**
```
https://philwegdata.github.io/dailynews/
```

## Step-by-Step Verification

### Step 1: Push the latest fixes

```bash
cd "/Users/phil/My Drive/18bresearch/dailynews"
git push
```

### Step 2: Enable GitHub Pages

1. Go to: https://github.com/philwegdata/dailynews/settings/pages
2. Source: **GitHub Actions**
3. Save

### Step 3: Run the workflow manually

1. Go to: https://github.com/philwegdata/dailynews/actions
2. Click **Daily News Aggregation**
3. Click **Run workflow** → **Run workflow**
4. Wait for it to complete (~2-3 minutes)

### Step 4: Check the logs

Look for:
```
Fetching from Industrial AI Podcast...
Fetching from IoT Use Case Podcast...
Fetching from Hacker News...
...
Fetched X total articles
Selected top 15 articles
```

### Step 5: Verify the data file

After workflow completes:
1. Go to: https://github.com/philwegdata/dailynews/tree/main/data
2. Check for `2026-01-04.json` (or today's date)
3. Click on it to view
4. Should see 15 articles with summaries

### Step 6: Wait for Pages deployment

1. After aggregation completes, Pages should deploy automatically
2. Check Actions tab for "Deploy to GitHub Pages" workflow
3. Wait ~2 minutes for deployment
4. Visit: https://philwegdata.github.io/dailynews/

## Common Error Messages

### "No module named 'backend'"

**Fix:** The workflow needs to set PYTHONPATH

Add to workflow before "Run aggregation":
```yaml
- name: Set PYTHONPATH
  run: echo "PYTHONPATH=$GITHUB_WORKSPACE" >> $GITHUB_ENV
```

### "Error fetching from [source]"

**Possible causes:**
- Source is down/unavailable
- RSS feed URL changed
- Network timeout in GitHub Actions

**Fix:**
- Check if source is accessible: `curl [RSS_URL]`
- Update URL in `plan` file if changed
- Increase timeout or add retry logic

### "API quota exceeded"

**Cause:** Too many Gemini API calls

**Fix:**
- Check quota at: https://aistudio.google.com
- Free tier: 15 RPM, 1M tokens/day
- Reduce number of sources or upgrade

### "403 Error" when pushing

**Already fixed!** Added `permissions: contents: write` to workflow

### "Pages deployment failed"

**Possible causes:**
- Pages not enabled
- Wrong source selected
- Build errors

**Fix:**
1. Check Settings → Pages → Source is "GitHub Actions"
2. Check Actions logs for specific error
3. Make sure `_site` directory is created correctly

## Expected Workflow Output

### Successful aggregation should show:

```
Fetching from Super Data Science...
Fetched 5 articles
Fetching from IoT Use Case Podcast...
Fetched 3 articles
Fetching from Industrial AI Podcast...
Fetched 2 articles
... (more sources)
Fetching from Hacker News...
Fetched 20 articles
Fetching from Hugging Face Daily Papers...
Fetched 10 articles

Fetched 60 total articles
Selected top 15 articles

Article 1: [title] - Score: 7.5
Article 2: [title] - Score: 6.0
... (summaries being generated)

Saved 15 articles to /home/runner/work/dailynews/dailynews/data/2026-01-04.json
Daily aggregation complete! Processed 15 articles
```

## Testing Locally

Before pushing, test locally:

```bash
cd "/Users/phil/My Drive/18bresearch/dailynews"
source .venv/bin/activate

# Test aggregation
python -m backend.aggregator

# Check output
cat data/$(date +%Y-%m-%d).json | jq '.articles[] | {title, source_name, score, summary}'
```

## Quick Checklist

- [ ] GitHub Pages enabled (Settings → Pages → Source: GitHub Actions)
- [ ] `GOOGLE_API_KEY` secret added
- [ ] Latest code pushed to GitHub
- [ ] Workflow ran successfully (check Actions tab)
- [ ] Data file created (check data/ folder on GitHub)
- [ ] Pages deployed (check Actions tab)
- [ ] Website accessible (visit URL)

## Still Having Issues?

1. **Check the Actions logs** - Most errors will be visible there
2. **Verify secrets** - Make sure API key is set correctly
3. **Test locally first** - Run `python -m backend.aggregator` locally
4. **Check source availability** - Some RSS feeds may be temporarily down
5. **Wait a bit** - GitHub Pages can take 5-10 minutes on first deploy

## Contact

If you're still stuck:
- Check the Actions logs for specific error messages
- Open an issue on GitHub with the error details
- Make sure all secrets are set correctly
