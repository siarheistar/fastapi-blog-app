from abc import ABC, abstractmethod
from typing import Optional, List

from .entities import User, Post, Session


class UserRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def add(self, user: User) -> User:
        raise NotImplementedError


class PostRepository(ABC):
    @abstractmethod
    def add(self, post: Post) -> Post:
        raise NotImplementedError

    @abstractmethod
    def list_recent(self, limit: int = 20) -> List[Post]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, post_id: int) -> Optional[Post]:
        raise NotImplementedError


class SessionRepository(ABC):
    @abstractmethod
    def add(self, session: Session) -> Session:
        raise NotImplementedError

    @abstractmethod
    def get(self, session_id: str) -> Optional[Session]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, session_id: str) -> None:
        raise NotImplementedError


class ImageStorageService(ABC):
    @abstractmethod
    def save_image(self, filename: str, data: bytes) -> str:
        """Save image and return relative path/URL."""
        raise NotImplementedError
