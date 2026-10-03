"""ztarcompress global constants."""

from pathlib import Path

# ztarcompress CONFIGURATION DIRECTORIES
BACKUP_DIR = Path.home() / ".local" / "share" / "ztarcompress" / "backups"
CONFIG_DIR = Path.home() / ".config" / "ztarcompress"
LOG_DIR = Path.home() / ".local" / "state" / "ztarcompress" / "logs"
CACHE_DIR = Path.home() / ".cache" / "ztarcompress"
