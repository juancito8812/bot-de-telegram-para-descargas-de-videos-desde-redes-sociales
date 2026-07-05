import os
from pathlib import Path

BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")
DOWNLOAD_DIR: Path = Path(os.environ.get("DOWNLOAD_DIR", "./downloads"))
MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50 MB Telegram limit
