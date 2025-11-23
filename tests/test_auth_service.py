from app.domain.entities import User, Session
from app.domain.interfaces import UserRepository, SessionRepository
from app.use_cases.auth_service import AuthService


class InMemoryUserRepo(UserRepository):
    def __init__(self) -> None:
        self.users: dict[str, User] = {}
        self._id_counter = 1

    def get_by_username(self, username: str) -> User | None:
        return self.users.get(username)

    def get_by_id(self, user_id: int) -> User | None:
        for user in self.users.values():
            if user.id == user_id:
                return user
        return None

    def add(self, user: User) -> User:
        user.id = self._id_counter
        self._id_counter += 1
        self.users[user.username] = user
        return user


class InMemorySessionRepo(SessionRepository):
    def __init__(self) -> None:
        self.sessions: dict[str, Session] = {}

    def add(self, session: Session) -> Session:
        self.sessions[session.id] = session
        return session

    def get(self, session_id: str) -> Session | None:
        return self.sessions.get(session_id)

    def delete(self, session_id: str) -> None:
        self.sessions.pop(session_id, None)


def test_register_and_authenticate() -> None:
    user_repo = InMemoryUserRepo()
    session_repo = InMemorySessionRepo()
    service = AuthService(user_repo=user_repo, session_repo=session_repo)

    user = service.register("alice", "password123")
    assert user.id is not None

    session = service.authenticate("alice", "password123")
    assert session is not None
    assert session_repo.get(session.id) is not None
