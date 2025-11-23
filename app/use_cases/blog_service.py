from typing import List, Optional

from app.domain.entities import Post
from app.domain.interfaces import PostRepository, ImageStorageService


class BlogService:
    def __init__(
        self,
        post_repo: PostRepository,
        image_storage: ImageStorageService,
    ) -> None:
        self._post_repo = post_repo
        self._image_storage = image_storage

    def create_post(
        self,
        author_id: int,
        title: str,
        content: str,
        image_filename: Optional[str] = None,
        image_bytes: Optional[bytes] = None,
    ) -> Post:
        image_path: Optional[str] = None
        if image_filename and image_bytes:
            image_path = self._image_storage.save_image(image_filename, image_bytes)
        post = Post(
            id=None,
            author_id=author_id,
            title=title,
            content=content,
            image_path=image_path,
        )
        return self._post_repo.add(post)

    def list_recent_posts(self, limit: int = 20) -> List[Post]:
        return self._post_repo.list_recent(limit=limit)

    def get_post(self, post_id: int) -> Optional[Post]:
        return self._post_repo.get_by_id(post_id)
