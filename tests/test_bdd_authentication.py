"""BDD step definitions for user authentication"""
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from app.domain.entities import User, Session
from app.domain.interfaces import UserRepository, SessionRepository
from app.use_cases.auth_service import AuthService
from tests.test_auth_service import InMemoryUserRepo, InMemorySessionRepo


# Load scenarios from feature file
scenarios("features/user_authentication.feature")


@pytest.fixture
def context() -> dict:
    """Shared context for test steps"""
    return {
        "user_repo": InMemoryUserRepo(),
        "session_repo": InMemorySessionRepo(),
        "current_user": None,
        "current_session": None,
        "error": None,
    }


@pytest.fixture
def auth_service(context: dict) -> AuthService:
    """Create auth service with in-memory repositories"""
    return AuthService(
        user_repo=context["user_repo"], session_repo=context["session_repo"]
    )


# Given steps


@given("the blog application is running")
def blog_app_running(context: dict, auth_service: AuthService) -> None:
    """Ensure the blog application context is set up"""
    context["auth_service"] = auth_service


@given(parsers.parse('a user exists with username "{username}" and password "{password}"'))
def user_exists(username: str, password: str, context: dict, auth_service: AuthService) -> None:
    """Create a user in the system"""
    user = auth_service.register(username, password)
    context["existing_user"] = user


@given(parsers.parse('I am logged in as "{username}"'))
def logged_in_as(username: str, context: dict, auth_service: AuthService) -> None:
    """Log in as a specific user"""
    # Get the user's password from context (assume it's the same as username for tests)
    user = context["user_repo"].get_by_username(username)
    if user:
        # We need to know the password - for test purposes, use stored test password
        session = auth_service.authenticate(username, "password123")
        context["current_session"] = session
        context["current_user"] = user


# When steps


@when(parsers.parse('I register with username "{username}" and password "{password}"'))
def register_user(username: str, password: str, context: dict, auth_service: AuthService) -> None:
    """Attempt to register a new user"""
    try:
        user = auth_service.register(username, password)
        context["current_user"] = user
        context["error"] = None
    except ValueError as e:
        context["error"] = str(e)
        context["current_user"] = None


@when(parsers.parse('I login with username "{username}" and password "{password}"'))
def login_user(username: str, password: str, context: dict, auth_service: AuthService) -> None:
    """Attempt to log in"""
    session = auth_service.authenticate(username, password)
    context["current_session"] = session
    if session:
        context["current_user"] = context["user_repo"].get_by_id(session.user_id)


@when("I logout")
def logout_user(context: dict, auth_service: AuthService) -> None:
    """Log out the current user"""
    if context.get("current_session"):
        auth_service.logout(context["current_session"].id)
        context["current_session"] = None


# Then steps


@then("the user should be created successfully")
def user_created_successfully(context: dict) -> None:
    """Verify user was created"""
    assert context["current_user"] is not None
    assert context["current_user"].id is not None


@then("the password should be hashed")
def password_is_hashed(context: dict) -> None:
    """Verify password is hashed"""
    user = context["current_user"]
    assert user is not None
    # Password hash should not be the plain password
    assert user.password_hash != "securepass123"
    # bcrypt hashes start with $2b$ or $2a$
    assert user.password_hash.startswith("$2")


@then(parsers.parse('the registration should fail with "{error_message}"'))
def registration_fails(error_message: str, context: dict) -> None:
    """Verify registration failed with expected error"""
    assert context["error"] is not None
    assert error_message in context["error"]


@then("a session should be created")
def session_created(context: dict) -> None:
    """Verify a session was created"""
    assert context["current_session"] is not None
    assert context["current_session"].id is not None


@then("I should be authenticated")
def user_authenticated(context: dict) -> None:
    """Verify user is authenticated"""
    assert context["current_session"] is not None
    assert context["current_user"] is not None


@then("the login should fail")
def login_fails(context: dict) -> None:
    """Verify login failed"""
    assert context["current_session"] is None


@then("no session should be created")
def no_session_created(context: dict) -> None:
    """Verify no session was created"""
    assert context["current_session"] is None


@then("my session should be deleted")
def session_deleted(context: dict) -> None:
    """Verify session was deleted"""
    # Session should no longer exist in repository
    sessions = context["session_repo"].sessions
    assert len(sessions) == 0


@then("I should not be authenticated")
def not_authenticated(context: dict) -> None:
    """Verify user is not authenticated"""
    assert context["current_session"] is None
