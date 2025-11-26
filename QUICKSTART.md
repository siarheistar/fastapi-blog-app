# Quick Start Guide

Get the blog app running in 5 minutes! ⚡

## For Experienced Developers

```bash
# 1. Clone the repository
git clone https://github.com/siarheistar/fastapi-blog-app.git
cd fastapi-blog-app

# 2. Set up virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Run the application
uvicorn app.main:app --reload --port 8000

# 4. Open in browser
# Visit: http://localhost:8000
```

## For First-Time Setup

**Need more detailed instructions?** See the [Complete Setup Guide](SETUP_GUIDE.md)

## Common Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the application
uvicorn app.main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=app

# Deactivate virtual environment
deactivate
```

## What's Next?

1. **Register a user** - Go to http://localhost:8000 and create an account
2. **Create a post** - Click "New Post" and write your first blog post
3. **Run tests** - Execute `pytest` to see all 35 tests pass
4. **Read the docs** - Check out [TESTING.md](TESTING.md) and [SETUP_GUIDE.md](SETUP_GUIDE.md)

## Troubleshooting

**Port already in use?**
```bash
uvicorn app.main:app --reload --port 8080
```

**Module not found?**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**Need help?** See [SETUP_GUIDE.md](SETUP_GUIDE.md#troubleshooting)
