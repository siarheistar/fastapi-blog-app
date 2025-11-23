import hashlib
import secrets
from typing import Optional

import bcrypt

from app.domain.entities import User, Session
from app.domain.interfaces import UserRepository, SessionRepository


MAX_PWD_LEN = 72


def _prepare_password(password: str) -> str:
    """Prepare password for bcrypt by ensuring it doesn't exceed 72 bytes.
    
    If password is too long, we hash it first with SHA256 and use the hex digest,
    which is exactly 64 bytes and deterministic.
    """
    raw = password.encode("utf-8")
    if len(raw) <= MAX_PWD_LEN:
        return password
    # Hash long passwords to get a fixed-length deterministic representation
    return hashlib.sha256(raw).hexdigest()


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        session_repo: SessionRepository,
    ) -> None:
        self._user_repo = user_repo
        self._session_repo = session_repo

    def register(self, username: str, password: str) -> User:
        existing = self._user_repo.get_by_username(username)
        if existing is not None:
            raise ValueError("Username already taken")
        password = _prepare_password(password)
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
        user = User(id=None, username=username, password_hash=password_hash)
        return self._user_repo.add(user)

    def authenticate(self, username: str, password: str) -> Optional[Session]:
        user = self._user_repo.get_by_username(username)
        if user is None:
            return None
        password = _prepare_password(password)
        password_bytes = password.encode('utf-8')
        password_hash_bytes = user.password_hash.encode('utf-8')
        if not bcrypt.checkpw(password_bytes, password_hash_bytes):
            return None
        session = Session(id=secrets.token_urlsafe(32), user_id=user.id)  # type: ignore[arg-type]
        return self._session_repo.add(session)

    def get_session(self, session_id: str) -> Optional[Session]:
        return self._session_repo.get(session_id)

    def logout(self, session_id: str) -> None:
        self._session_repo.delete(session_id)
