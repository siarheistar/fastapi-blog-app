from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    username: str
    password_hash: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Post:
    id: Optional[int]
    author_id: int
    title: str
    content: str
    image_path: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Session:
    id: str
    user_id: int
    created_at: datetime = field(default_factory=datetime.utcnow)
