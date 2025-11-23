from pathlib import Path
import uuid

from app.domain.interfaces import ImageStorageService


class LocalImageStorage(ImageStorageService):
    def __init__(self, base_dir: Path) -> None:
        self._base_dir = base_dir
        self._base_dir.mkdir(parents=True, exist_ok=True)

    def save_image(self, filename: str, data: bytes) -> str:
        ext = Path(filename).suffix
        unique_name = f"{uuid.uuid4().hex}{ext}"
        target_path = self._base_dir / unique_name
        target_path.write_bytes(data)
        return unique_name
