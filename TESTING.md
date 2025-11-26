# Testing Documentation

## Overview

This project includes comprehensive test coverage with **93% code coverage** across unit tests, integration tests, API tests, and BDD (Behavior-Driven Development) tests.

## Test Structure

```
tests/
├── features/                       # BDD feature files (Gherkin syntax)
│   ├── user_authentication.feature
│   └── blog_posts.feature
├── test_auth_service.py           # Unit tests for authentication service
├── test_blog_service.py           # Unit tests for blog service
├── test_api.py                    # API/Integration tests
├── test_bdd_authentication.py     # BDD step definitions for auth
└── test_bdd_blog_posts.py         # BDD step definitions for blog posts
```

## Test Types

### 1. Unit Tests
Unit tests verify individual components in isolation using in-memory implementations of repositories.

**Files:**
- `test_auth_service.py` - Tests for user registration, login, logout
- `test_blog_service.py` - Tests for post creation, listing, retrieval

**Run unit tests only:**
```bash
pytest tests/test_auth_service.py tests/test_blog_service.py
```

### 2. API/Integration Tests
API tests verify the entire application stack including HTTP endpoints, request/response handling, and authentication flows.

**File:** `test_api.py`

**Test Coverage:**
- Homepage rendering
- User registration and login flows
- Post creation and viewing
- Authentication requirements
- Static file serving

**Run API tests only:**
```bash
pytest tests/test_api.py
```

### 3. BDD (Behavior-Driven Development) Tests
BDD tests use Gherkin syntax to describe features in plain English and verify them with step definitions.

**Files:**
- `features/user_authentication.feature` - User registration and login scenarios
- `features/blog_posts.feature` - Blog post management scenarios
- `test_bdd_authentication.py` - Step definitions for authentication
- `test_bdd_blog_posts.py` - Step definitions for blog posts

**Run BDD tests only:**
```bash
pytest tests/test_bdd_*.py
```

## Running Tests

### Quick Start

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests with coverage
pytest

# Or use the test runner script
./run_tests.sh
```

### Advanced Options

```bash
# Run tests with verbose output
pytest -v

# Run tests with extra verbose output
pytest -vv

# Run tests and show print statements
pytest -s

# Run specific test file
pytest tests/test_api.py

# Run specific test class
pytest tests/test_blog_service.py::TestBlogService

# Run specific test function
pytest tests/test_api.py::TestAuthentication::test_login_with_valid_credentials

# Run tests matching a pattern
pytest -k "test_create"

# Run tests with coverage report
pytest --cov=app --cov-report=html

# Stop on first failure
pytest -x

# Run last failed tests only
pytest --lf
```

## Test Coverage

Current coverage: **93%**

View detailed coverage report:
```bash
# Generate HTML report
pytest --cov=app --cov-report=html

# Open in browser
open htmlcov/index.html
```

### Coverage Breakdown

| Module | Coverage |
|--------|----------|
| app/api/routers_auth.py | 100% |
| app/api/dependencies.py | 95% |
| app/api/routers_posts.py | 91% |
| app/infrastructure/repositories.py | 97% |
| app/use_cases/auth_service.py | 95% |
| app/use_cases/blog_service.py | 100% |
| app/domain/entities.py | 100% |
| app/main.py | 100% |

## Test Fixtures

### Available Fixtures

**Authentication:**
- `user_repo` - In-memory user repository
- `session_repo` - In-memory session repository
- `auth_service` - Authentication service instance

**Blog:**
- `post_repo` - In-memory post repository
- `image_storage` - In-memory image storage
- `blog_service` - Blog service instance

**API:**
- `client` - Async HTTP client for testing FastAPI endpoints

**BDD:**
- `context` - Shared context dictionary for step definitions

## Writing Tests

### Unit Test Example

```python
def test_create_post(blog_service: BlogService) -> None:
    """Test creating a blog post"""
    post = blog_service.create_post(
        author_id=1,
        title="Test Post",
        content="Test content"
    )

    assert post.id is not None
    assert post.title == "Test Post"
```

### API Test Example

```python
@pytest.mark.asyncio
async def test_login(client: AsyncClient) -> None:
    """Test user login"""
    response = await client.post(
        "/auth/login",
        data={"username": "user", "password": "pass"}
    )

    assert response.status_code == 302
```

### BDD Feature Example

```gherkin
Scenario: User creates a blog post
    Given the blog application is running
    And a user exists with username "blogger" and password "pass"
    And I am logged in as "blogger"
    When I create a post with title "My Post" and content "Content"
    Then the post should be created successfully
```

## Continuous Integration

The test suite is configured to run automatically in CI/CD pipelines:

```yaml
# .github/workflows/ci.yml
- name: Run tests
  run: |
    pytest --cov=app --cov-report=xml
```

## Test Configuration

Tests are configured in `pytest.ini`:

- **Coverage threshold**: Aim for >90%
- **Async mode**: Automatic
- **Coverage reports**: Terminal, HTML, and XML formats
- **Test markers**: unit, integration, api, bdd, slow, asyncio

## Dependencies

Testing tools and libraries:
- `pytest` - Test framework
- `pytest-cov` - Coverage plugin
- `pytest-bdd` - BDD testing
- `pytest-asyncio` - Async test support
- `httpx` - Async HTTP client
- `faker` - Test data generation

## Best Practices

1. **Isolation**: Each test should be independent and not rely on other tests
2. **Clarity**: Test names should clearly describe what they test
3. **Coverage**: Aim for >90% code coverage
4. **Speed**: Keep tests fast by using in-memory implementations
5. **Maintenance**: Update tests when features change
6. **Documentation**: Use docstrings to explain complex test scenarios

## Troubleshooting

### Tests failing after code changes
- Run tests with `-vv` for detailed output
- Check if fixtures need updating
- Verify database schema matches entities

### Coverage not updating
- Delete `.coverage` file and `htmlcov/` directory
- Run `pytest --cov=app --cov-report=html` again

### Async tests failing
- Ensure `@pytest.mark.asyncio` decorator is present
- Check that fixtures are properly async/await

## Test Results

**Latest Test Run:**
- ✅ 35 tests passed
- ⏱️  Execution time: ~7 seconds
- 📊 Coverage: 93%
- ⚠️  4 deprecation warnings (non-critical)

## Next Steps

To improve coverage further:
1. Add tests for error handling edge cases
2. Test image upload with various file types
3. Add performance/load tests
4. Test concurrent user sessions
5. Add security tests for SQL injection, XSS, etc.
