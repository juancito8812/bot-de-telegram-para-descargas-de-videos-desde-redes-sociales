import os
from pathlib import Path

BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")
DOWNLOAD_DIR: Path = Path(os.environ.get("DOWNLOAD_DIR", "./downloads"))
MAX_FILE_SIZE: int = int(os.environ.get("MAX_FILE_SIZE", 0))  # 0 = sin limite (Local Bot API)
TELEGRAM_API_URL: str = os.environ.get("TELEGRAM_API_URL", "")  # vacio = cloud API

# ── Logging ───────────────────────────────────
LOG_DIR: Path = Path(os.environ.get("LOG_DIR", "logs"))
LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_MAX_BYTES: int = 5 * 1024 * 1024   # 5 MB por archivo
LOG_BACKUP_COUNT: int = 3               # mantener 3 rotaciones
