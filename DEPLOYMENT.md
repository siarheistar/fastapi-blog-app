# Deployment Guide

This guide will help you deploy your FastAPI blog app to various hosting platforms.

## Quick Deployment Options Comparison

| Platform | Free Tier | Database | Setup Difficulty | Best For |
|----------|-----------|----------|------------------|----------|
| Render.com | ✅ 750hrs/mo | SQLite/PostgreSQL | Easy | Beginners |
| Railway.app | ✅ $5 credit/mo | Any | Easy | Quick deploys |
| Fly.io | ✅ 3 VMs | Any | Medium | Docker users |
| PythonAnywhere | ✅ Limited | SQLite | Medium | Simple projects |
| Heroku | ❌ Paid only | Any | Easy | Production apps |

## Option 1: Render.com (Recommended for Beginners)

### Prerequisites
- GitHub account
- Your code pushed to GitHub

### Steps

1. **Create a Render account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create a new Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Give it a name (e.g., `my-blog-app`)

3. **Configure the service**
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

4. **Add persistent disk (for SQLite)**
   - In service settings, go to "Disks"
   - Add disk mounted at `/opt/render/project/src/app_data`
   - Size: 1GB (free)

5. **Deploy**
   - Click "Create Web Service"
   - Wait 2-5 minutes for deployment
   - Your app will be live at `https://your-app-name.onrender.com`

### Important Notes
- Free tier apps sleep after 15 mins of inactivity
- First request after sleep takes ~30 seconds
- Upgrade to paid tier for always-on service

## Option 2: Railway.app

### Prerequisites
- GitHub account
- Your code pushed to GitHub

### Steps

1. **Sign up at Railway**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create new project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure (if needed)**
   - Railway auto-detects Python
   - It will use the `Procfile` automatically
   - Set environment variables if needed

4. **Deploy**
   - Railway deploys automatically
   - Get your URL from the deployment settings

### Environment Variables
Add these in Railway settings if needed:
```
PORT=8000  # Railway sets this automatically
```

## Option 3: Fly.io

### Prerequisites
- Fly.io CLI installed
- Docker Desktop (optional but recommended)

### Steps

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login to Fly**
   ```bash
   fly auth login
   ```

3. **Launch your app**
   ```bash
   cd /path/to/your/project
   fly launch
   ```

4. **Follow the prompts**
   - Name your app
   - Choose region
   - Don't deploy PostgreSQL (we're using SQLite)
   - Deploy? Yes

5. **Your app is live!**
   - URL: `https://your-app-name.fly.dev`

### Fly.io Configuration

If `fly launch` doesn't auto-configure, create `fly.toml`:

```toml
app = "your-app-name"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8000"

[[services]]
  internal_port = 8000
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

[mounts]
  source = "app_data"
  destination = "/app/app_data"
```

## Option 4: PythonAnywhere

### Prerequisites
- PythonAnywhere account (free tier available)

### Steps

1. **Sign up**
   - Go to https://www.pythonanywhere.com
   - Create free account

2. **Upload your code**
   - Use "Files" tab to upload
   - Or use Git: `git clone your-repo-url`

3. **Create virtual environment**
   ```bash
   cd ~/your-project
   python3.9 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Web App**
   - Go to "Web" tab
   - Add new web app
   - Choose "Manual configuration"
   - Python 3.9

5. **Configure WSGI file**
   Edit the WSGI configuration file:
   ```python
   import sys
   path = '/home/yourusername/your-project'
   if path not in sys.path:
       sys.path.append(path)

   from app.main import app as application
   ```

6. **Reload and test**

## Environment Variables

For all platforms, you may want to set these environment variables:

```bash
# Optional: Set to production
ENVIRONMENT=production

# Optional: Database URL (if using PostgreSQL)
DATABASE_URL=postgresql://user:pass@host:port/db

# Optional: Secret key for sessions
SECRET_KEY=your-secret-key-here
```

## Upgrading Database to PostgreSQL (Production)

For production deployments, consider PostgreSQL:

1. **Update requirements.txt**
   ```
   psycopg2-binary==2.9.9
   ```

2. **Update database connection in app/infrastructure/db.py**
   ```python
   import os
   
   DATABASE_URL = os.getenv(
       "DATABASE_URL",
       "sqlite:///./app_data/blog.db"
   )
   ```

3. **Set DATABASE_URL in your hosting platform**

## Monitoring Your Deployment

After deployment:

1. **Test the registration flow**
   - Create a new account
   - Login
   - Create a post

2. **Check logs**
   - Most platforms provide log viewing
   - Look for errors or warnings

3. **Monitor performance**
   - Response times
   - Error rates
   - Uptime

## Troubleshooting

### App won't start
- Check logs for Python errors
- Verify `requirements.txt` has all dependencies
- Ensure start command is correct

### Database errors
- Check if persistent disk is mounted (Render)
- Verify database file permissions
- For SQLite, ensure directory exists

### Static files not loading
- Check static file paths in templates
- Verify `/static` mount in main.py
- Check hosting platform static file settings

### Port binding errors
- Use `--host 0.0.0.0` in uvicorn command
- Use `--port $PORT` to read from environment
- Don't hardcode port 8000

## Cost Optimization

### Free Tier Limitations
- Most free tiers have sleep/downtime
- Limited compute resources
- Bandwidth caps
- Storage limits

### When to Upgrade
- High traffic (>100 daily users)
- Need 24/7 uptime
- Require faster response times
- Need more storage

## Security Checklist

Before going to production:

- [ ] Use HTTPS (enabled by default on most platforms)
- [ ] Set strong session secrets
- [ ] Use environment variables for secrets
- [ ] Enable CORS only for trusted domains
- [ ] Keep dependencies updated
- [ ] Use PostgreSQL instead of SQLite
- [ ] Implement rate limiting
- [ ] Add logging and monitoring

## Need Help?

If you encounter issues:

1. Check the hosting platform's documentation
2. Review application logs
3. Test locally first with the same configuration
4. Search for error messages
5. Open an issue on GitHub

---

**Note**: This guide is current as of 2025. Hosting platform features and pricing may change.
