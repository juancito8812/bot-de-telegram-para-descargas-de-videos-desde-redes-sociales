import os
from pathlib import Path

BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")
DOWNLOAD_DIR: Path = Path(os.environ.get("DOWNLOAD_DIR", "./downloads"))
MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50 MB Telegram limit

# ── Logging ───────────────────────────────────
LOG_DIR: Path = Path(os.environ.get("LOG_DIR", "logs"))
LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_MAX_BYTES: int = 5 * 1024 * 1024   # 5 MB por archivo
LOG_BACKUP_COUNT: int = 3               # mantener 3 rotaciones
