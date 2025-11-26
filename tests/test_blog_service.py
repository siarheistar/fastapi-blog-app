"""Unit tests for BlogService"""
from typing import Optional, List, Dict
import pytest

from app.domain.entities import Post
from app.domain.interfaces import PostRepository, ImageStorageService
from app.use_cases.blog_service import BlogService


class InMemoryPostRepo(PostRepository):
    """In-memory implementation of PostRepository for testing"""

    def __init__(self) -> None:
        self.posts: Dict[int, Post] = {}
        self._id_counter = 1

    def add(self, post: Post) -> Post:
        post.id = self._id_counter
        self._id_counter += 1
        self.posts[post.id] = post
        return post

    def get_by_id(self, post_id: int) -> Optional[Post]:
        return self.posts.get(post_id)

    def list_recent(self, limit: int = 20) -> List[Post]:
        sorted_posts = sorted(
            self.posts.values(),
            key=lambda p: p.created_at if p.created_at else "",
            reverse=True,
        )
        return sorted_posts[:limit]


class InMemoryImageStorage(ImageStorageService):
    """In-memory implementation of ImageStorageService for testing"""

    def __init__(self) -> None:
        self.images: Dict[str, bytes] = {}

    def save_image(self, filename: str, data: bytes) -> str:
        """Save image and return the storage path"""
        path = f"test_{filename}"
        self.images[path] = data
        return path


@pytest.fixture
def post_repo() -> InMemoryPostRepo:
    """Fixture for post repository"""
    return InMemoryPostRepo()


@pytest.fixture
def image_storage() -> InMemoryImageStorage:
    """Fixture for image storage"""
    return InMemoryImageStorage()


@pytest.fixture
def blog_service(
    post_repo: InMemoryPostRepo, image_storage: InMemoryImageStorage
) -> BlogService:
    """Fixture for blog service"""
    return BlogService(post_repo=post_repo, image_storage=image_storage)


class TestBlogService:
    """Test cases for BlogService"""

    def test_create_post_without_image(self, blog_service: BlogService) -> None:
        """Test creating a post without an image"""
        post = blog_service.create_post(
            author_id=1, title="Test Post", content="Test content"
        )

        assert post.id is not None
        assert post.author_id == 1
        assert post.title == "Test Post"
        assert post.content == "Test content"
        assert post.image_path is None

    def test_create_post_with_image(
        self, blog_service: BlogService, image_storage: InMemoryImageStorage
    ) -> None:
        """Test creating a post with an image"""
        image_data = b"fake_image_data"
        post = blog_service.create_post(
            author_id=1,
            title="Photo Post",
            content="Check this out",
            image_filename="photo.jpg",
            image_bytes=image_data,
        )

        assert post.id is not None
        assert post.image_path is not None
        assert post.image_path == "test_photo.jpg"
        assert image_storage.images[post.image_path] == image_data

    def test_create_post_with_filename_but_no_bytes(
        self, blog_service: BlogService
    ) -> None:
        """Test that image is not saved if only filename is provided"""
        post = blog_service.create_post(
            author_id=1,
            title="No Image",
            content="Content",
            image_filename="file.jpg",
            image_bytes=None,
        )

        assert post.image_path is None

    def test_list_recent_posts(self, blog_service: BlogService) -> None:
        """Test listing recent posts"""
        # Create multiple posts
        for i in range(5):
            blog_service.create_post(
                author_id=1, title=f"Post {i}", content=f"Content {i}"
            )

        posts = blog_service.list_recent_posts(limit=20)
        assert len(posts) == 5

    def test_list_recent_posts_with_limit(self, blog_service: BlogService) -> None:
        """Test listing recent posts with a limit"""
        # Create 10 posts
        for i in range(10):
            blog_service.create_post(
                author_id=1, title=f"Post {i}", content=f"Content {i}"
            )

        posts = blog_service.list_recent_posts(limit=3)
        assert len(posts) == 3

    def test_get_existing_post(self, blog_service: BlogService) -> None:
        """Test retrieving an existing post"""
        created_post = blog_service.create_post(
            author_id=1, title="Findable", content="You can find me"
        )

        found_post = blog_service.get_post(created_post.id)
        assert found_post is not None
        assert found_post.id == created_post.id
        assert found_post.title == "Findable"

    def test_get_non_existent_post(self, blog_service: BlogService) -> None:
        """Test retrieving a non-existent post returns None"""
        post = blog_service.get_post(9999)
        assert post is None

    def test_multiple_authors(self, blog_service: BlogService) -> None:
        """Test posts from multiple authors"""
        post1 = blog_service.create_post(
            author_id=1, title="Author 1 Post", content="Content 1"
        )
        post2 = blog_service.create_post(
            author_id=2, title="Author 2 Post", content="Content 2"
        )

        assert post1.author_id == 1
        assert post2.author_id == 2
        assert post1.id != post2.id

    def test_empty_post_list(self, blog_service: BlogService) -> None:
        """Test listing posts when no posts exist"""
        posts = blog_service.list_recent_posts()
        assert len(posts) == 0
        assert posts == []
