# Deploy to Render.com - Step by Step Guide

Since **GitHub Pages only hosts static sites** and cannot run Python/FastAPI applications, follow this guide to deploy to **Render.com** (free tier available).

## Why Not GitHub Pages?

❌ GitHub Pages limitations:
- Only serves static HTML/CSS/JavaScript
- Cannot run Python backend code
- Cannot execute FastAPI server
- No database support

✅ Render.com advantages:
- Free tier with 750 hours/month
- Runs Python applications
- Supports SQLite with persistent storage
- Easy GitHub integration
- Automatic deployments on git push

## Prerequisites

- Your code is on GitHub: ✅ https://github.com/siarheistar/fastapi-blog-app
- A free Render.com account (create one below)

## Step-by-Step Deployment

### Step 1: Create Render Account

1. Go to https://render.com
2. Click "Get Started"
3. Sign up with your GitHub account (recommended)
4. Authorize Render to access your GitHub repositories

### Step 2: Create New Web Service

1. From Render Dashboard, click **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect to your GitHub repository:
   - Click "Configure account" if needed
   - Search for `fastapi-blog-app`
   - Click **"Connect"**

### Step 3: Configure Your Service

Fill in the following settings:

**Basic Settings:**
- **Name**: `fastapi-blog-app` (or your preferred name)
- **Region**: Choose closest to you (e.g., Oregon, Frankfurt)
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Environment**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

**Instance Type:**
- Select **"Free"** ($0/month)

### Step 4: Add Persistent Disk (Important!)

To keep your SQLite database between deployments:

1. Scroll down to **"Disks"** section
2. Click **"Add Disk"**
3. Configure:
   - **Name**: `app-data`
   - **Mount Path**: `/opt/render/project/src/app_data`
   - **Size**: `1 GB` (free tier)
4. Click **"Save"**

### Step 5: Add Environment Variables (Optional)

If you want to customize settings:

1. Scroll to **"Environment Variables"**
2. Add variables (optional):
   ```
   ENVIRONMENT=production
   ```

### Step 6: Deploy!

1. Click **"Create Web Service"** button at bottom
2. Render will start building and deploying
3. Watch the logs - deployment takes 2-5 minutes
4. Once you see "Your service is live", it's ready!

### Step 7: Access Your App

Your app will be available at:
```
https://fastapi-blog-app.onrender.com
```

(Replace `fastapi-blog-app` with your service name)

## Post-Deployment

### Test Your App

1. Visit your Render URL
2. Create an account (register)
3. Login with your credentials
4. Create a test blog post
5. Upload an image
6. Verify everything works!

### Important Notes

⚠️ **Free Tier Limitations:**
- Service sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- 750 hours/month free (enough for testing/personal use)
- Limited to 512 MB RAM

💡 **Upgrade to Paid Tier** ($7/month) for:
- Always-on service (no sleep)
- More RAM and CPU
- Better performance
- 24/7 availability

### Automatic Deployments

✅ **Good news!** Render automatically redeploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update feature"
git push origin main

# Render automatically detects and redeploys!
```

## Monitoring Your App

### View Logs

1. Go to Render Dashboard
2. Click on your service
3. Click **"Logs"** tab
4. See real-time application logs

### Check Health

1. In service dashboard, check **"Events"** tab
2. Monitor deploy status
3. Check for errors

## Troubleshooting

### Service Won't Start

**Check the logs for errors:**
```
Failed to bind to port
```
**Solution**: Ensure start command uses `$PORT` variable

**Error**: `Module not found`
**Solution**: Check `requirements.txt` has all dependencies

### Database Errors

**Error**: `no such table`
**Solution**: Disk might not be mounted. Check disk configuration.

**Error**: `database is locked`
**Solution**: SQLite limitation. Consider upgrading to PostgreSQL for production.

### Static Files Not Loading

**Error**: CSS/images not loading
**Solution**: Check that `/static` directory exists and is configured in `main.py`

## Upgrading to PostgreSQL (Optional)

For production apps, PostgreSQL is recommended:

### 1. Create PostgreSQL Database in Render

1. Click "New +" → "PostgreSQL"
2. Configure and create
3. Copy the "Internal Database URL"

### 2. Update Your App

Add to `requirements.txt`:
```
psycopg2-binary==2.9.9
```

Update `app/infrastructure/db.py`:
```python
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./app_data/blog.db"
)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
```

### 3. Add Environment Variable

In your Render service:
- Add env var `DATABASE_URL` = your PostgreSQL URL

## Custom Domain (Optional)

To use your own domain:

1. Go to service settings
2. Click **"Custom Domain"**
3. Add your domain
4. Update DNS settings as instructed

## Cost Breakdown

| Plan | Price | RAM | Always On | Support |
|------|-------|-----|-----------|---------|
| Free | $0 | 512MB | ❌ (sleeps) | Community |
| Starter | $7/mo | 512MB | ✅ | Email |
| Standard | $25/mo | 2GB | ✅ | Priority |

## Next Steps

✅ Your app is deployed!
✅ GitHub auto-deploys on push
✅ Free hosting with Render

### Share Your App

Your blog is live at: `https://your-service.onrender.com`

Share it with friends and start blogging!

## Need Help?

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **GitHub Issues**: https://github.com/siarheistar/fastapi-blog-app/issues

---

**Note**: This guide assumes you're using the free tier. For production use, consider the paid tier for better performance and 24/7 uptime.
