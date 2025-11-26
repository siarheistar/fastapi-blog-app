# Complete Setup Guide

This guide will walk you through setting up the FastAPI Blog application on a new computer from scratch.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Clone the Repository](#clone-the-repository)
3. [Set Up Development Environment](#set-up-development-environment)
4. [Run the Application Locally](#run-the-application-locally)
5. [Run Tests](#run-tests)
6. [Database Management](#database-management)
7. [Troubleshooting](#troubleshooting)
8. [IDE Setup](#ide-setup)
9. [Next Steps](#next-steps)

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software

#### 1. Python 3.9 or Higher

**Check if Python is installed:**
```bash
python3 --version
```

**Install Python:**

- **macOS:**
  ```bash
  brew install python@3.9
  ```
  Or download from [python.org](https://www.python.org/downloads/)

- **Ubuntu/Debian:**
  ```bash
  sudo apt update
  sudo apt install python3.9 python3.9-venv python3-pip
  ```

- **Windows:**
  Download from [python.org](https://www.python.org/downloads/) and run the installer.
  ⚠️ Make sure to check "Add Python to PATH" during installation.

#### 2. Git

**Check if Git is installed:**
```bash
git --version
```

**Install Git:**

- **macOS:**
  ```bash
  brew install git
  ```
  Or download from [git-scm.com](https://git-scm.com/)

- **Ubuntu/Debian:**
  ```bash
  sudo apt install git
  ```

- **Windows:**
  Download from [git-scm.com](https://git-scm.com/)

#### 3. SQLite3 (Usually pre-installed)

**Check if SQLite is installed:**
```bash
sqlite3 --version
```

If not installed:
- **macOS:** Pre-installed
- **Ubuntu/Debian:** `sudo apt install sqlite3`
- **Windows:** Download from [sqlite.org](https://www.sqlite.org/download.html)

---

## Clone the Repository

### Step 1: Choose a Directory

Navigate to where you want to store the project:

```bash
cd ~/Projects  # or any directory you prefer
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/siarheistar/fastapi-blog-app.git
cd fastapi-blog-app
```

### Step 3: Verify the Clone

```bash
ls -la
```

You should see:
```
.github/
app/
tests/
scripts/
README.md
requirements.txt
...
```

---

## Set Up Development Environment

### Step 1: Create a Virtual Environment

**Why?** Virtual environments isolate project dependencies from your system Python.

```bash
python3 -m venv .venv
```

This creates a `.venv` directory containing the isolated Python environment.

### Step 2: Activate the Virtual Environment

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

💡 **Tip:** You'll see `(.venv)` appear in your terminal prompt when activated.

### Step 3: Upgrade pip

```bash
pip install --upgrade pip
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages including:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- SQLAlchemy (database ORM)
- Pytest (testing framework)
- And more...

**Installation will take 1-2 minutes.**

### Step 5: Verify Installation

```bash
pip list
```

You should see ~50+ packages installed.

---

## Run the Application Locally

### Step 1: Ensure Virtual Environment is Active

```bash
# If not active, activate it:
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

### Step 2: Start the Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

**What do these flags mean?**
- `--reload`: Auto-reload on code changes
- `--port 8000`: Run on port 8000

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 3: Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:8000
```

or

```
http://localhost:8000
```

You should see the beautiful blog homepage! 🎉

### Step 4: Create Your First User

1. Click on "Register" or scroll to the registration form
2. Enter a username and password
3. Click "Register"
4. You'll be redirected and logged in automatically

### Step 5: Create Your First Post

1. Click the "New Post" button
2. Add a title and content
3. Optionally upload an image
4. Click "Publish Post"

### Step 6: Stop the Server

Press `CTRL+C` in the terminal to stop the server.

---

## Run Tests

The project includes comprehensive tests with 91% code coverage.

### Step 1: Ensure Virtual Environment is Active

```bash
source .venv/bin/activate  # macOS/Linux
```

### Step 2: Run All Tests

**Quick method:**
```bash
pytest
```

**With the test runner script:**
```bash
chmod +x run_tests.sh  # First time only
./run_tests.sh
```

**Expected output:**
```
================================ test session starts ================================
platform darwin -- Python 3.9.10, pytest-8.3.3, pluggy-1.6.0
collected 35 items

tests/test_api.py ..............                                          [ 40%]
tests/test_auth_service.py .                                              [ 42%]
tests/test_bdd_authentication.py .....                                    [ 57%]
tests/test_bdd_blog_posts.py ......                                       [ 74%]
tests/test_blog_service.py .........                                      [100%]

======================== 35 passed, 4 warnings in 5.35s ========================
================================ tests coverage ================================
Coverage: 91%
```

### Step 3: Run Specific Test Types

**Unit tests only:**
```bash
pytest tests/test_auth_service.py tests/test_blog_service.py
```

**API tests only:**
```bash
pytest tests/test_api.py
```

**BDD tests only:**
```bash
pytest tests/test_bdd_*.py
```

**Run tests with verbose output:**
```bash
pytest -v
```

**Run tests with extra verbose output:**
```bash
pytest -vv
```

**Stop on first failure:**
```bash
pytest -x
```

### Step 4: View Coverage Report

**Generate HTML coverage report:**
```bash
pytest --cov=app --cov-report=html
```

**Open the report:**
```bash
# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html

# Windows
start htmlcov/index.html
```

This opens an interactive coverage report in your browser showing which lines are covered by tests.

### Step 5: Run Tests with Different Options

**Show print statements:**
```bash
pytest -s
```

**Run tests matching a pattern:**
```bash
pytest -k "test_create"
```

**Run specific test:**
```bash
pytest tests/test_api.py::TestAuthentication::test_login_with_valid_credentials
```

---

## Database Management

### Understanding the Database

The application uses SQLite, a file-based database stored at:
```
app_data/blog.db
```

The database is automatically created when you first run the application.

### View Database Contents

**Using SQLite command-line:**
```bash
sqlite3 app_data/blog.db
```

**Common SQLite commands:**
```sql
-- List all tables
.tables

-- View all users
SELECT * FROM users;

-- View all posts
SELECT * FROM posts;

-- View all sessions
SELECT * FROM sessions;

-- Exit
.quit
```

### Reset the Database

**Option 1: Delete the database file**
```bash
rm -f app_data/blog.db
```

The database will be recreated automatically when you restart the app.

**Option 2: Delete specific data**
```bash
sqlite3 app_data/blog.db "DELETE FROM posts;"
sqlite3 app_data/blog.db "DELETE FROM users;"
```

### Backup the Database

```bash
cp app_data/blog.db app_data/blog.db.backup
```

### Restore a Backup

```bash
cp app_data/blog.db.backup app_data/blog.db
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "command not found: python3"

**Solution:**
```bash
# Try using 'python' instead of 'python3'
python --version

# If that doesn't work, install Python
```

#### Issue 2: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue 3: "Address already in use"

**Solution:**
```bash
# Port 8000 is already in use. Use a different port:
uvicorn app.main:app --reload --port 8080

# Or find and kill the process using port 8000:
# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

#### Issue 4: "Permission denied" when running scripts

**Solution:**
```bash
chmod +x run_tests.sh
chmod +x scripts/*.sh
```

#### Issue 5: Tests failing with "ImportError"

**Solution:**
```bash
# Make sure you're in the project root directory
pwd  # Should show .../fastapi-blog-app

# Reinstall test dependencies
pip install -r requirements.txt
```

#### Issue 6: Virtual environment not activating on Windows PowerShell

**Solution:**
```powershell
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.venv\Scripts\Activate.ps1
```

#### Issue 7: "Database is locked"

**Solution:**
```bash
# Close any open SQLite connections
# Restart the application
# If that doesn't work, remove and recreate the database
rm -f app_data/blog.db
```

---

## IDE Setup

### Visual Studio Code

**Recommended Extensions:**
1. Python (Microsoft)
2. Pylance (Microsoft)
3. Python Test Explorer
4. GitLens
5. Better Comments

**Open the project:**
```bash
code .
```

**Select Python Interpreter:**
1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Python: Select Interpreter"
3. Choose the interpreter from `.venv` folder

**Run tests in VS Code:**
1. Click the test flask icon in the sidebar
2. Click "Configure Python Tests"
3. Select "pytest"
4. Tests will appear in the Test Explorer

### PyCharm

**Open the project:**
```bash
# Open PyCharm and select "Open" → Navigate to project folder
```

**Configure Python Interpreter:**
1. Go to Settings/Preferences → Project → Python Interpreter
2. Click the gear icon → Add
3. Select "Existing environment"
4. Choose `.venv/bin/python` (Mac/Linux) or `.venv\Scripts\python.exe` (Windows)

**Run tests in PyCharm:**
1. Right-click on `tests` folder → "Run pytest in tests"

---

## Next Steps

### Development Workflow

1. **Make sure you're on the latest code:**
   ```bash
   git pull origin main
   ```

2. **Create a new branch for your feature:**
   ```bash
   git checkout -b feature/my-new-feature
   ```

3. **Make your changes**

4. **Run tests:**
   ```bash
   pytest
   ```

5. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add new feature"
   ```

6. **Push to GitHub:**
   ```bash
   git push origin feature/my-new-feature
   ```

7. **Create a Pull Request on GitHub**

### Project Structure

```
fastapi-blog-app/
├── app/                        # Main application code
│   ├── api/                   # API routes and dependencies
│   │   ├── dependencies.py    # Dependency injection
│   │   ├── routers_auth.py    # Authentication routes
│   │   └── routers_posts.py   # Blog post routes
│   ├── domain/                # Domain entities and interfaces
│   │   ├── entities.py        # User, Post, Session entities
│   │   └── interfaces.py      # Repository interfaces
│   ├── infrastructure/        # Database and storage
│   │   ├── db.py             # Database configuration
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── repositories.py   # Repository implementations
│   │   └── storage_local.py  # Image storage
│   ├── use_cases/            # Business logic
│   │   ├── auth_service.py   # Authentication logic
│   │   └── blog_service.py   # Blog logic
│   ├── web/                  # Frontend templates and static files
│   │   ├── static/           # CSS and uploaded images
│   │   └── templates/        # Jinja2 HTML templates
│   └── main.py               # FastAPI application entry point
├── tests/                     # Test suite
│   ├── features/             # BDD feature files
│   ├── test_api.py          # API integration tests
│   ├── test_auth_service.py # Auth unit tests
│   ├── test_blog_service.py # Blog unit tests
│   └── test_bdd_*.py        # BDD step definitions
├── scripts/                  # Utility scripts
├── .venv/                   # Virtual environment (created)
├── app_data/                # SQLite database (created)
├── requirements.txt         # Python dependencies
├── pytest.ini              # Test configuration
└── README.md               # Project documentation
```

### Learn More

- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **SQLAlchemy Tutorial:** https://docs.sqlalchemy.org/
- **Pytest Documentation:** https://docs.pytest.org/
- **Jinja2 Templates:** https://jinja.palletsprojects.com/

### Deploy Your Application

See deployment guides:
- [README.md](README.md) - Quick deployment options
- [PYTHONANYWHERE_WSGI_FIX.md](PYTHONANYWHERE_WSGI_FIX.md) - PythonAnywhere setup

### Testing Documentation

For detailed testing information:
- [TESTING.md](TESTING.md) - Comprehensive testing guide

---

## Quick Reference Card

### Daily Commands

```bash
# Activate virtual environment
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows

# Run the application
uvicorn app.main:app --reload --port 8000

# Run tests
pytest

# Run tests with coverage
pytest --cov=app

# Update dependencies
pip install -r requirements.txt

# Check code status
git status

# Pull latest changes
git pull origin main

# Deactivate virtual environment
deactivate
```

### Access Points

- **Local Application:** http://localhost:8000
- **Live Application:** https://fastapi-blog-app.fly.dev
- **GitHub Repository:** https://github.com/siarheistar/fastapi-blog-app
- **API Documentation:** http://localhost:8000/docs (when running locally)

---

## Need Help?

- **Found a bug?** Open an issue on [GitHub](https://github.com/siarheistar/fastapi-blog-app/issues)
- **Have questions?** Check the [README.md](README.md) or [TESTING.md](TESTING.md)
- **Want to contribute?** See the development workflow above

---

**Happy Coding! 🚀**
