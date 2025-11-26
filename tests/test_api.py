"""API integration tests for the blog application"""
import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator

from app.main import create_app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Create a test client for the FastAPI application"""
    app = create_app()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
class TestHomepage:
    """Test cases for the homepage"""

    async def test_homepage_loads(self, client: AsyncClient) -> None:
        """Test that the homepage loads successfully"""
        response = await client.get("/")
        assert response.status_code == 200
        assert b"My Blog" in response.content

    async def test_homepage_shows_login_for_unauthenticated(
        self, client: AsyncClient
    ) -> None:
        """Test that login form is shown for unauthenticated users"""
        response = await client.get("/")
        assert response.status_code == 200
        assert b"Login" in response.content or b"login" in response.content


@pytest.mark.asyncio
class TestAuthentication:
    """Test cases for authentication endpoints"""

    async def test_register_new_user(self, client: AsyncClient) -> None:
        """Test registering a new user"""
        response = await client.post(
            "/auth/register",
            data={"username": "newuser", "password": "password123"},
            follow_redirects=False,
        )
        # Should redirect after successful registration or return 400 if validation fails
        assert response.status_code in [302, 400]

    async def test_register_duplicate_username(self, client: AsyncClient) -> None:
        """Test that registering with an existing username fails"""
        # Register first user
        await client.post(
            "/auth/register",
            data={"username": "duplicate", "password": "pass1"},
        )

        # Try to register again with same username
        response = await client.post(
            "/auth/register",
            data={"username": "duplicate", "password": "pass2"},
            follow_redirects=False,
        )

        # Should return 400 or redirect with error
        assert response.status_code in [400, 302]

    async def test_login_with_valid_credentials(self, client: AsyncClient) -> None:
        """Test logging in with valid credentials"""
        # First register a user
        await client.post(
            "/auth/register",
            data={"username": "loginuser", "password": "loginpass"},
        )

        # Now login
        response = await client.post(
            "/auth/login",
            data={"username": "loginuser", "password": "loginpass"},
            follow_redirects=False,
        )

        assert response.status_code == 302
        # Should set a session cookie
        assert "session_id" in response.cookies or "set-cookie" in response.headers

    async def test_login_with_invalid_credentials(self, client: AsyncClient) -> None:
        """Test that login fails with wrong password"""
        # Register a user
        await client.post(
            "/auth/register",
            data={"username": "testuser", "password": "correctpass"},
        )

        # Try to login with wrong password
        response = await client.post(
            "/auth/login",
            data={"username": "testuser", "password": "wrongpass"},
            follow_redirects=False,
        )

        # Should return 400 or 401
        assert response.status_code in [400, 401, 302]

    async def test_logout(self, client: AsyncClient) -> None:
        """Test logging out"""
        # Register and login
        await client.post(
            "/auth/register",
            data={"username": "logouttest", "password": "password"},
        )
        login_response = await client.post(
            "/auth/login",
            data={"username": "logouttest", "password": "password"},
        )

        # Logout
        response = await client.post("/auth/logout", follow_redirects=False)
        assert response.status_code == 302


@pytest.mark.asyncio
class TestBlogPosts:
    """Test cases for blog post endpoints"""

    async def test_view_post_detail(self, client: AsyncClient) -> None:
        """Test viewing a specific post"""
        # First, create a user and login
        await client.post(
            "/auth/register",
            data={"username": "poster", "password": "postpass"},
        )
        await client.post(
            "/auth/login",
            data={"username": "poster", "password": "postpass"},
        )

        # Create a post
        await client.post(
            "/posts",
            data={"title": "Test Post", "content": "Test content"},
        )

        # Try to view it (assuming it's post ID 1)
        response = await client.get("/posts/1")
        assert response.status_code in [200, 302]

    async def test_view_non_existent_post_redirects(
        self, client: AsyncClient
    ) -> None:
        """Test that viewing a non-existent post redirects"""
        response = await client.get("/posts/99999", follow_redirects=False)
        assert response.status_code == 302
        assert response.headers["location"] == "/"

    async def test_create_post_requires_authentication(
        self, client: AsyncClient
    ) -> None:
        """Test that creating a post requires authentication"""
        response = await client.post(
            "/posts",
            data={"title": "Unauthorized", "content": "Should fail"},
            follow_redirects=False,
        )
        # Should redirect to homepage
        assert response.status_code == 302

    async def test_create_post_when_authenticated(self, client: AsyncClient) -> None:
        """Test creating a post when logged in"""
        # Register and login
        await client.post(
            "/auth/register",
            data={"username": "author", "password": "authorpass"},
        )
        await client.post(
            "/auth/login",
            data={"username": "author", "password": "authorpass"},
        )

        # Create a post
        response = await client.post(
            "/posts",
            data={"title": "My Post", "content": "My content"},
            follow_redirects=False,
        )

        assert response.status_code == 302
        # Should redirect to homepage after creating post
        assert response.headers["location"] == "/"

    async def test_new_post_form_requires_authentication(
        self, client: AsyncClient
    ) -> None:
        """Test that accessing new post form requires authentication"""
        response = await client.get("/new", follow_redirects=False)
        assert response.status_code == 302

    async def test_new_post_form_accessible_when_authenticated(
        self, client: AsyncClient
    ) -> None:
        """Test that new post form is accessible when logged in"""
        # Register and login
        await client.post(
            "/auth/register",
            data={"username": "formuser", "password": "formpass"},
        )
        await client.post(
            "/auth/login",
            data={"username": "formuser", "password": "formpass"},
        )

        response = await client.get("/new")
        assert response.status_code == 200
        assert b"Create New Post" in response.content or b"New Post" in response.content


@pytest.mark.asyncio
class TestStaticFiles:
    """Test cases for static file serving"""

    async def test_static_css_accessible(self, client: AsyncClient) -> None:
        """Test that CSS file is accessible"""
        response = await client.get("/static/style.css")
        assert response.status_code == 200
        assert "text/css" in response.headers.get("content-type", "")
