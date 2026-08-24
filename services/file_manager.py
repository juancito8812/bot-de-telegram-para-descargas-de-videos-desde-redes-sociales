import asyncio
import tempfile
import shutil
import os
from pathlib import Path

# ponytail: aiofiles eliminado — asyncio.to_thread + os.remove basta.
# Si se agregan mas operaciones async de I/O, reconsiderar aiofiles.


async def ensure_download_dir(path: Path) -> None:
    """Create download directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def get_temp_path(suffix: str = ".mp4") -> Path:
    """Return a unique temporary file path with the given suffix."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    return Path(path)


async def cleanup_file(path: Path) -> None:
    """Delete a file or directory if it exists. No-op if missing."""
    try:
        if path.is_dir():
            await asyncio.to_thread(shutil.rmtree, path)
        else:
            # Also clean parent temp dir if it's the only file
            parent = path.parent
            await asyncio.to_thread(os.remove, path)
            # Remove empty temp dir (mkdtemp-created)
            if parent.exists() and not any(parent.iterdir()):
                await asyncio.to_thread(parent.rmdir)
    except FileNotFoundError:
        pass


def is_within_limit(file_size: int, max_bytes: int = 50 * 1024 * 1024) -> bool:
    """Check if file size is within Telegram's upload limit (default 50MB)."""
    return file_size <= max_bytes
