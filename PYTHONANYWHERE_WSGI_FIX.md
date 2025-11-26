# PythonAnywhere WSGI Configuration Fix

## Problem
FastAPI is an ASGI application, but PythonAnywhere's free tier uses WSGI servers. This causes the error:
```
TypeError: __call__() missing 1 required positional argument: 'send'
```

## Solution

### Step 1: Install asgiref
Open a Bash console on PythonAnywhere and run:
```bash
cd ~/fastapi-blog-app
source venv/bin/activate
pip install asgiref
```

### Step 2: Update WSGI Configuration
Edit your WSGI configuration file at `/var/www/siarheistar_pythonanywhere_com_wsgi.py`:

```python
import sys
from pathlib import Path

# Add your project directory to the sys.path
project_home = '/home/siarheistar/fastapi-blog-app'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Add the virtual environment's site-packages
venv_site_packages = '/home/siarheistar/fastapi-blog-app/venv/lib/python3.9/site-packages'
if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)

# Import the ASGI-to-WSGI adapter
from asgiref.wsgi import WsgiToAsgi

# Import your FastAPI app
from app.main import app

# Wrap the ASGI app (FastAPI) to make it WSGI-compatible
application = WsgiToAsgi(app)
```

### Step 3: Reload Your Web App
- Go to the Web tab on PythonAnywhere
- Click the green "Reload" button

## What This Does
- `WsgiToAsgi` is a wrapper that converts ASGI applications (like FastAPI) to work with WSGI servers
- It translates between the WSGI `(environ, start_response)` interface and the ASGI `(scope, receive, send)` interface
- This allows FastAPI to run on PythonAnywhere's WSGI infrastructure

## Verification
After reloading, visit your site at `https://siarheistar.pythonanywhere.com`

You should see your blog homepage without errors!

## Important Notes
- This adapter has some performance overhead compared to native ASGI servers
- For production with higher traffic, consider using platforms with native ASGI support (like Fly.io with uvicorn)
- PythonAnywhere's free tier is great for learning and small projects
