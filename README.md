# FastAPI Blog App

A beautiful, modern blog web application with user authentication, post creation, and image uploads. Built with FastAPI, SQLite, and styled with a modern purple gradient theme.

## Features

- User registration and authentication with bcrypt password hashing
- Session-based auth via secure HTTP-only cookies
- Create and publish blog posts with optional image uploads
- View all posts on a beautiful homepage with card layouts
- Individual post detail pages
- Responsive design with smooth animations
- SQLite database via SQLAlchemy ORM
- Modern UI with glassmorphism effects and gradient backgrounds

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git (for version control)

## Local Installation & Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd test_website
```

### 2. Set up the virtual environment

Run the bootstrap script to create a virtual environment and install dependencies:

```bash
chmod +x scripts/bootstrap_env.sh
./scripts/bootstrap_env.sh
```

Or manually:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start the development server

```bash
source .venv/bin/activate  # If not already activated
uvicorn app.main:app --reload --port 8000
```

### 4. Access the application

Open your browser and navigate to:
```
http://127.0.0.1:8000
```

You should see the beautiful homepage with login/registration forms!

## Usage

1. **Register a new account**: Fill in the registration form with a username and password
2. **Login**: Use your credentials to login
3. **Create a post**: Click "New Post" button, add a title, content, and optionally upload an image
4. **View posts**: Browse all posts on the homepage or click on individual posts to read more

## Running Tests

This project includes comprehensive test coverage (93%) with unit tests, API tests, and BDD tests.

**Quick Start:**
```bash
source .venv/bin/activate
pytest
```

**Or use the test runner:**
```bash
./run_tests.sh
```

**View coverage report:**
```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

For detailed testing documentation, see [TESTING.md](TESTING.md)

## Project Structure

```
test_website/
├── app/
│   ├── api/              # API routes and dependencies
│   ├── domain/           # Domain entities and interfaces
│   ├── infrastructure/   # Database models and repositories
│   ├── use_cases/        # Business logic (auth, blog services)
│   ├── web/             # Templates and static files
│   │   ├── static/      # CSS and uploaded images
│   │   └── templates/   # HTML Jinja2 templates
│   └── main.py          # FastAPI application entry point
├── tests/               # Unit tests
├── scripts/             # Setup and deployment scripts
└── requirements.txt     # Python dependencies
```

## Deployment Options

**Important**: GitHub Pages only hosts static HTML/CSS/JS sites and **cannot run Python/FastAPI backends**. Here are recommended hosting platforms:

### Recommended Free Hosting Platforms

#### 1. **Render.com** (Recommended - Free tier available)
- Free tier with 750 hours/month
- Easy deployment from GitHub
- Supports SQLite (with persistent disk)
- Steps:
  1. Create account at https://render.com
  2. Create new Web Service
  3. Connect your GitHub repository
  4. Set build command: `pip install -r requirements.txt`
  5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  6. Add environment variables if needed
  7. Deploy!

#### 2. **Railway.app** (Free tier available)
- $5 free credit monthly
- GitHub integration
- Steps:
  1. Sign up at https://railway.app
  2. Create new project from GitHub repo
  3. Railway auto-detects Python and deploys
  4. Add Procfile if needed: `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### 3. **Fly.io** (Free tier available) - RECOMMENDED
- 3 shared-cpu VMs free with persistent storage
- Native ASGI support (no adapter needed)
- Steps:
  1. Install flyctl: `curl -L https://fly.io/install.sh | sh` (or `brew install flyctl` on Mac)
  2. Login: `fly auth login`
  3. Create volume: `fly volumes create app_data --size 1`
  4. Deploy: `fly deploy`

Your app is already configured with [fly.toml](fly.toml)

#### 4. **PythonAnywhere** (Free tier available)
- Free tier with limitations
- Good for small projects
- Requires manual setup through web interface

#### 5. **Heroku** (Paid after Nov 2022)
- No longer has free tier, but reliable paid option
- Easy GitHub integration
- Create `Procfile`: `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Production Considerations

Before deploying to production:

1. **Database**: Consider upgrading from SQLite to PostgreSQL for production
2. **Environment Variables**: Use `.env` file for secrets (add to `.gitignore`)
3. **Static Files**: Configure a CDN or object storage for uploaded images
4. **HTTPS**: Ensure your hosting platform provides SSL certificates
5. **CORS**: Configure CORS settings if needed
6. **Secret Key**: Set a secure secret key for session management

## GitHub Actions CI/CD

- `.github/workflows/ci.yml` - Runs tests on pushes/PRs to `main`
- `.github/workflows/deploy.yml` - Packages the app as an artifact

## Create GitHub Repository

Requires the GitHub CLI (`gh`) to be installed and authenticated.

```bash
cd /Users/sergei/Projects/test_website
chmod +x scripts/*.sh
./scripts/create_repo_and_push.sh YOUR_GH_USERNAME blog-website
```

This will create the repo `YOUR_GH_USERNAME/blog-website`, push the code, and trigger CI.

## Technologies Used

- **Backend**: FastAPI (Python web framework)
- **Database**: SQLite + SQLAlchemy ORM
- **Authentication**: bcrypt for password hashing
- **Frontend**: Jinja2 templates, HTML5, CSS3
- **Styling**: Custom CSS with gradients and animations
- **Testing**: pytest

## License

MIT License (or your preferred license)

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
