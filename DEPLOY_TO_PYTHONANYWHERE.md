# Deploy to PythonAnywhere - Free Forever

## Why PythonAnywhere?

✅ **Actually free forever:**
- No trial period
- No credit card required
- No expiration
- **Never shuts down**

✅ **Perfect for beginners:**
- Web-based interface
- Built-in file editor
- Easy setup
- Great for learning

✅ **Persistent storage:**
- SQLite works perfectly
- File uploads persist
- 512MB storage on free tier

⚠️ **Limitations:**
- Slower performance
- Custom domains require paid tier
- Your URL: `yourusername.pythonanywhere.com`

## Step-by-Step Setup

### Step 1: Create Account

1. Go to https://www.pythonanywhere.com
2. Click "Pricing & signup"
3. Choose "Create a Beginner account" (FREE)
4. Fill in your details (no credit card needed!)
5. Verify your email

### Step 2: Upload Your Code

**Option A: Use Git (Recommended)**

1. Open a **Bash console** from PythonAnywhere dashboard
2. Clone your repository:

```bash
git clone https://github.com/siarheistar/fastapi-blog-app.git
cd fastapi-blog-app
```

**Option B: Upload files manually**

1. Go to "Files" tab
2. Create directory: `fastapi-blog-app`
3. Upload your files

### Step 3: Create Virtual Environment

In the Bash console:

```bash
cd ~/fastapi-blog-app
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Set Up Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select **Python 3.9**

### Step 5: Configure WSGI

1. On the Web tab, find "Code" section
2. Click on WSGI configuration file link
3. Replace ALL content with:

```python
import sys
import os

# Add your project directory to path
project_home = '/home/yourusername/fastapi-blog-app'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtual environment
activate_this = os.path.join(project_home, 'venv/bin/activate_this.py')
with open(activate_this) as file:
    exec(file.read(), dict(__file__=activate_this))

# Import FastAPI app
from app.main import app as application
```

**Important:** Replace `yourusername` with your actual PythonAnywhere username!

### Step 6: Set Virtual Environment Path

1. In Web tab, find "Virtualenv" section
2. Enter path: `/home/yourusername/fastapi-blog-app/venv`
3. Replace `yourusername` with your username

### Step 7: Create Static Files Mapping

1. In Web tab, find "Static files" section
2. Add mapping:
   - URL: `/static`
   - Directory: `/home/yourusername/fastapi-blog-app/app/web/static`

### Step 8: Reload & Test

1. Click big green "Reload" button
2. Click on your URL: `https://yourusername.pythonanywhere.com`
3. Your blog should be live! 🎉

## Managing Your App

### Update Code

```bash
# In Bash console
cd ~/fastapi-blog-app
git pull origin main
```

Then click "Reload" on Web tab.

### View Logs

1. Go to Web tab
2. Click on "Log files" links:
   - Error log
   - Server log
   - Access log

### Access Database

```bash
# In Bash console
cd ~/fastapi-blog-app
sqlite3 app_data/blog.db
```

### Backup Database

```bash
# Download from Files tab
cp app_data/blog.db ~/backups/blog_$(date +%Y%m%d).db
```

## Free Tier Details

| Feature | Free Tier |
|---------|-----------|
| Cost | **$0 forever** |
| CPU | Limited |
| Storage | 512MB |
| Always On | ✅ Yes |
| Custom Domain | ❌ No |
| HTTPS | ✅ Yes |
| Database | SQLite ✅ |

## Limitations

⚠️ **Free tier restrictions:**
- Can't make external HTTPS requests
- Slower than paid platforms
- No custom domains
- URL: `yourusername.pythonanywhere.com`
- Limited CPU seconds

💡 **Good enough for:**
- Personal blogs
- Learning projects
- Portfolio sites
- Small communities

## Upgrade Options

If you need more:

**Hacker Plan** ($5/month):
- 512MB storage
- Custom domains
- External HTTPS allowed

**Web Developer** ($12/month):
- 1GB storage
- More CPU time
- Better performance

## Troubleshooting

### 502 Bad Gateway

Check error logs on Web tab. Usually means:
- Wrong WSGI configuration
- Virtual environment path incorrect
- Import errors

### Static files not loading

Check static files mapping on Web tab. Path should be absolute.

### Database errors

Ensure `app_data/` directory exists:
```bash
mkdir -p ~/fastapi-blog-app/app_data
```

### Module not found errors

Reinstall dependencies:
```bash
cd ~/fastapi-blog-app
source venv/bin/activate
pip install -r requirements.txt
```

## Comparison

| Feature | PythonAnywhere | Railway | Fly.io |
|---------|---------------|---------|--------|
| **Free Forever** | ✅ Yes | ❌ Trial only | ✅ Yes |
| **No Credit Card** | ✅ Yes | Varies | ✅ Yes |
| **Always On** | ✅ Yes | ❌ After trial | ⚠️ Auto-sleep |
| **Setup Difficulty** | Medium | Easy | Medium |
| **Performance** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Best For** | Beginners | Production | Scaling apps |

## Your Blog URL

After setup:
```
https://yourusername.pythonanywhere.com
```

Replace `yourusername` with your PythonAnywhere username.

## Support

- **Help**: https://help.pythonanywhere.com
- **Forums**: https://www.pythonanywhere.com/forums/
- **Docs**: https://help.pythonanywhere.com/pages/

---

**This is the easiest free-forever option!** Perfect for personal blogs and learning.
