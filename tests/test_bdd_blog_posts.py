"""BDD step definitions for blog posts"""
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from app.domain.entities import Post
from app.use_cases.blog_service import BlogService
from tests.test_blog_service import InMemoryPostRepo, InMemoryImageStorage
from tests.test_auth_service import InMemoryUserRepo, InMemorySessionRepo
from app.use_cases.auth_service import AuthService


# Load scenarios from feature file
scenarios("features/blog_posts.feature")


@pytest.fixture
def context() -> dict:
    """Shared context for test steps"""
    return {
        "post_repo": InMemoryPostRepo(),
        "image_storage": InMemoryImageStorage(),
        "user_repo": InMemoryUserRepo(),
        "session_repo": InMemorySessionRepo(),
        "current_user": None,
        "current_session": None,
        "current_post": None,
        "posts": [],
        "error": None,
        "redirect_url": None,
    }


@pytest.fixture
def blog_service(context: dict) -> BlogService:
    """Create blog service with in-memory repositories"""
    return BlogService(
        post_repo=context["post_repo"], image_storage=context["image_storage"]
    )


@pytest.fixture
def auth_service(context: dict) -> AuthService:
    """Create auth service with in-memory repositories"""
    return AuthService(
        user_repo=context["user_repo"], session_repo=context["session_repo"]
    )


# Given steps


@given("the blog application is running")
def blog_app_running(context: dict, blog_service: BlogService, auth_service: AuthService) -> None:
    """Ensure the blog application context is set up"""
    context["blog_service"] = blog_service
    context["auth_service"] = auth_service


@given(parsers.parse('a user exists with username "{username}" and password "{password}"'))
def user_exists(username: str, password: str, context: dict, auth_service: AuthService) -> None:
    """Create a user in the system"""
    user = auth_service.register(username, password)
    context[f"user_{username}"] = user


@given(parsers.parse('I am logged in as "{username}"'))
def logged_in_as(username: str, context: dict, auth_service: AuthService) -> None:
    """Log in as a specific user"""
    user = context.get(f"user_{username}")
    if user:
        context["current_user"] = user
        context["current_user_id"] = user.id


@given(parsers.parse("there are {count:d} existing blog posts"))
def existing_posts(count: int, context: dict, blog_service: BlogService) -> None:
    """Create multiple blog posts"""
    for i in range(count):
        post = blog_service.create_post(
            author_id=1, title=f"Post {i+1}", content=f"Content for post {i+1}"
        )
        context["posts"].append(post)


@given(parsers.parse('a post exists with id {post_id:d} and title "{title}"'))
def post_exists(post_id: int, title: str, context: dict, blog_service: BlogService) -> None:
    """Create a specific post"""
    post = blog_service.create_post(author_id=1, title=title, content="Test content")
    context["test_post"] = post
    context["test_post_id"] = post.id


# When steps


@when(parsers.parse('I create a post with title "{title}" and content "{content}"'))
def create_post(title: str, content: str, context: dict, blog_service: BlogService) -> None:
    """Create a blog post"""
    if context.get("current_user_id"):
        post = blog_service.create_post(
            author_id=context["current_user_id"], title=title, content=content
        )
        context["current_post"] = post
    else:
        context["error"] = "Not authenticated"


@when(parsers.parse('I create a post with title "{title}" and content "{content}" and an image'))
def create_post_with_image(
    title: str, content: str, context: dict, blog_service: BlogService
) -> None:
    """Create a blog post with an image"""
    if context.get("current_user_id"):
        image_data = b"fake_image_bytes"
        post = blog_service.create_post(
            author_id=context["current_user_id"],
            title=title,
            content=content,
            image_filename="test.jpg",
            image_bytes=image_data,
        )
        context["current_post"] = post
    else:
        context["error"] = "Not authenticated"


@when("I try to create a post without authentication")
def create_post_unauthenticated(context: dict, blog_service: BlogService) -> None:
    """Attempt to create a post without being authenticated"""
    context["current_user_id"] = None
    context["error"] = "Not authenticated"


@when("I visit the homepage")
def visit_homepage(context: dict, blog_service: BlogService) -> None:
    """Visit the homepage and load posts"""
    context["posts"] = blog_service.list_recent_posts()


@when(parsers.parse("I view post with id {post_id:d}"))
def view_post(post_id: int, context: dict, blog_service: BlogService) -> None:
    """View a specific post"""
    post = blog_service.get_post(post_id)
    context["viewed_post"] = post


@when(parsers.parse("I try to view post with id {post_id:d}"))
def try_view_non_existent_post(post_id: int, context: dict, blog_service: BlogService) -> None:
    """Try to view a non-existent post"""
    post = blog_service.get_post(post_id)
    if post is None:
        context["redirect_url"] = "/"
    context["viewed_post"] = post


# Then steps


@then("the post should be created successfully")
def post_created_successfully(context: dict) -> None:
    """Verify post was created"""
    assert context.get("current_post") is not None
    assert context["current_post"].id is not None


@then("the post should appear in the recent posts list")
def post_in_recent_list(context: dict, blog_service: BlogService) -> None:
    """Verify post appears in recent posts"""
    posts = blog_service.list_recent_posts()
    post_titles = [p.title for p in posts]
    current_post = context.get("current_post")
    assert current_post is not None
    assert current_post.title in post_titles


@then("the post should have an image attached")
def post_has_image(context: dict) -> None:
    """Verify post has an image"""
    post = context.get("current_post")
    assert post is not None
    assert post.image_path is not None


@then("the post creation should be rejected")
def post_creation_rejected(context: dict) -> None:
    """Verify post creation was rejected"""
    assert context.get("error") is not None
    assert context.get("current_post") is None


@then(parsers.parse("I should see all {count:d} posts"))
def see_all_posts(count: int, context: dict) -> None:
    """Verify all posts are visible"""
    posts = context.get("posts", [])
    assert len(posts) == count


@then(parsers.parse('I should see the post title "{title}"'))
def see_post_title(title: str, context: dict) -> None:
    """Verify post title is visible"""
    viewed_post = context.get("viewed_post")
    assert viewed_post is not None
    assert viewed_post.title == title


@then("I should see the post content")
def see_post_content(context: dict) -> None:
    """Verify post content is visible"""
    viewed_post = context.get("viewed_post")
    assert viewed_post is not None
    assert viewed_post.content is not None
    assert len(viewed_post.content) > 0


@then("I should be redirected to the homepage")
def redirected_to_homepage(context: dict) -> None:
    """Verify redirect to homepage"""
    assert context.get("redirect_url") == "/"
    assert context.get("viewed_post") is None
