from typing import Optional, List

from sqlalchemy.orm import Session

from app.domain.entities import User, Post, Session as DomainSession
from app.domain.interfaces import (
    UserRepository,
    PostRepository,
    SessionRepository,
)
from .models import UserModel, PostModel, SessionModel


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self._db = db

    def get_by_username(self, username: str) -> Optional[User]:
        row = (
            self._db.query(UserModel)
            .filter(UserModel.username == username)
            .one_or_none()
        )
        if row is None:
            return None
        return User(
            id=row.id,
            username=row.username,
            password_hash=row.password_hash,
            created_at=row.created_at,
        )

    def get_by_id(self, user_id: int) -> Optional[User]:
        row = self._db.get(UserModel, user_id)
        if row is None:
            return None
        return User(
            id=row.id,
            username=row.username,
            password_hash=row.password_hash,
            created_at=row.created_at,
        )

    def add(self, user: User) -> User:
        row = UserModel(
            username=user.username,
            password_hash=user.password_hash,
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        user.id = row.id
        return user


class SqlAlchemyPostRepository(PostRepository):
    def __init__(self, db: Session):
        self._db = db

    def add(self, post: Post) -> Post:
        row = PostModel(
            author_id=post.author_id,
            title=post.title,
            content=post.content,
            image_path=post.image_path,
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        post.id = row.id
        return post

    def list_recent(self, limit: int = 20) -> List[Post]:
        rows = (
            self._db.query(PostModel)
            .order_by(PostModel.created_at.desc())
            .limit(limit)
            .all()
        )
        return [
            Post(
                id=row.id,
                author_id=row.author_id,
                title=row.title,
                content=row.content,
                image_path=row.image_path,
                created_at=row.created_at,
            )
            for row in rows
        ]

    def get_by_id(self, post_id: int) -> Optional[Post]:
        row = self._db.get(PostModel, post_id)
        if row is None:
            return None
        return Post(
            id=row.id,
            author_id=row.author_id,
            title=row.title,
            content=row.content,
            image_path=row.image_path,
            created_at=row.created_at,
        )


class SqlAlchemySessionRepository(SessionRepository):
    def __init__(self, db: Session):
        self._db = db

    def add(self, session: DomainSession) -> DomainSession:
        row = SessionModel(id=session.id, user_id=session.user_id)
        self._db.add(row)
        self._db.commit()
        return session

    def get(self, session_id: str) -> Optional[DomainSession]:
        row = self._db.get(SessionModel, session_id)
        if row is None:
            return None
        return DomainSession(id=row.id, user_id=row.user_id, created_at=row.created_at)

    def delete(self, session_id: str) -> None:
        row = self._db.get(SessionModel, session_id)
        if row is not None:
            self._db.delete(row)
            self._db.commit()
