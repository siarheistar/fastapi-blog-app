from pathlib import Path
from typing import Generator, Optional

from fastapi import Cookie, Depends
from sqlalchemy.orm import Session

from app.domain.interfaces import (
    UserRepository,
    PostRepository,
    SessionRepository,
    ImageStorageService,
)
from app.infrastructure.db import SessionLocal
from app.infrastructure.repositories import (
    SqlAlchemyUserRepository,
    SqlAlchemyPostRepository,
    SqlAlchemySessionRepository,
)
from app.infrastructure.storage_local import LocalImageStorage
from app.use_cases.auth_service import AuthService
from app.use_cases.blog_service import BlogService


UPLOAD_DIR = Path(__file__).resolve().parent.parent / "web" / "static" / "uploads"


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:  # type: ignore[override]
    return SqlAlchemyUserRepository(db)


def get_post_repo(db: Session = Depends(get_db)) -> PostRepository:  # type: ignore[override]
    return SqlAlchemyPostRepository(db)


def get_session_repo(db: Session = Depends(get_db)) -> SessionRepository:  # type: ignore[override]
    return SqlAlchemySessionRepository(db)


def get_image_storage() -> ImageStorageService:  # type: ignore[override]
    return LocalImageStorage(UPLOAD_DIR)


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repo),  # type: ignore[assignment]
    session_repo: SessionRepository = Depends(get_session_repo),  # type: ignore[assignment]
) -> AuthService:
    return AuthService(user_repo=user_repo, session_repo=session_repo)


def get_blog_service(
    post_repo: PostRepository = Depends(get_post_repo),  # type: ignore[assignment]
    image_storage: ImageStorageService = Depends(get_image_storage),  # type: ignore[assignment]
) -> BlogService:
    return BlogService(post_repo=post_repo, image_storage=image_storage)


class CurrentUser:
    def __init__(
        self,
        id: int,
        username: str,
    ) -> None:
        self.id = id
        self.username = username


async def get_current_user(
    session_id: Optional[str] = Cookie(default=None, alias="session_id"),
    auth_service: AuthService = Depends(get_auth_service),
    user_repo: UserRepository = Depends(get_user_repo),  # type: ignore[assignment]
) -> Optional[CurrentUser]:
    if not session_id:
        return None
    session = auth_service.get_session(session_id)
    if session is None:
        return None
    user = user_repo.get_by_id(session.user_id)
    if user is None:
        return None
    return CurrentUser(id=user.id, username=user.username)  # type: ignore[arg-type]
