"""Configuration management for ztarcompress."""

import tomllib
from typing import cast

from .constants import BACKUP_DIR, CACHE_DIR, CONFIG_DIR, LOG_DIR
from .models import AppConfig, ErrorCode, make_error


def init_config_dirs() -> None:
    """Initialize the configuration directories for ztarcompress.

    This function creates the necessary directories for storing backups,
    configuration files, logs, and cache files. It ensures that the required
    directory structure exists in the user's home directory.

    Raises:
        RuntimeError: If any of the directories cannot be created due to
        permission issues or other errors.
    """

    # Create the directories if they do not exist
    for directory in [
        BACKUP_DIR,
        CONFIG_DIR,
        LOG_DIR,
        CACHE_DIR,
    ]:
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except PermissionError as exc:
            message = make_error(
                ErrorCode.PERMISSION_DENIED, path=str(directory)
            )
            raise RuntimeError(message.message) from exc
        except OSError as exc:
            message = make_error(
                ErrorCode.SOURCE_NOT_FOUND, path=str(directory)
            )
            raise RuntimeError(message.message) from exc
        except Exception as exc:
            message = make_error(ErrorCode.UNKNOWN_ERROR, path=str(directory))
            raise RuntimeError(message.message) from exc


# create config.toml
def write_default_config() -> None:
    """Write the default configuration to config.toml.

    This function creates a default configuration file in the user's
    configuration directory. If the file already exists, it will not be
    overwritten.

    Raises:
        RuntimeError: If the configuration file cannot be created or written.
    """
    config_file = CONFIG_DIR / "config.toml"

    if not config_file.exists():
        default_config = """# ztarcompress configuration file

# Version: Configuration file version for compatibility (default: 1)
# DO NOT EDIT THIS VALUE
config_version = 1

# Sources: List of directories to back up (default: ~/Documents, ~/.config)
sources = ["~/Documents", "~/.config",]

# Exclusions: List of directories or files to exclude from the backup
# (default: node_modules, .venv, __pycache__, .ruff_cache)
exclude = ["**/node_modules", "**/.venv", "**/__pycache__", "**/.ruff_cache"]

# Directories for ztarcompress
# Backup directory: Where to store the backups (default: ~/Backups)
# Configuration directory: Path to the configuration directory (default: ~/.config/ztarcompress/)
# Log directory: Where to store log files (default: ~/.local/state/ztarcompress/logs)
# Cache directory: Where to store cache files (default: ~/.cache/ztarcompress)
backup_directory = "~/.local/share/ztarcompress/backups"
config_directory = "~/.config/ztarcompress/"
log_directory = "~/.local/state/ztarcompress/logs"
cache_directory = "~/.cache/ztarcompress"

# Metadata settings
# Metadata retention: How many metadata records to keep (default: 10)
metadata_retention = 10

# Retention settings
# Archive retention: How many archive files to keep (default: 2)
# Encrypted archive retention: How many encrypted archive files to keep (default: 1)
# Decrypted archive retention: How many decrypted archive files to keep (default: 1)
# Extracted archive retention: How many extracted archive files to keep (default: 1)
archive_retention = 2
encrypted_archive_retention = 1
decrypted_archive_retention = 1
extracted_archive_retention = 1
"""
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with config_file.open("w") as file:
                file.write(default_config)
        except PermissionError as exc:
            message = make_error(
                ErrorCode.PERMISSION_DENIED, path=str(config_file)
            )
            raise RuntimeError(message.message) from exc
        except OSError as exc:
            message = make_error(
                ErrorCode.SOURCE_NOT_FOUND, path=str(config_file)
            )
            raise RuntimeError(message.message) from exc
        except Exception as exc:
            message = make_error(
                ErrorCode.UNKNOWN_ERROR, path=str(config_file)
            )
            raise RuntimeError(message.message) from exc


# read config.toml
def read_config() -> AppConfig:
    """Read the config from config.toml.

    This function read the configuration file and returns the
    configuration as a dictionary. If the file does not exist, it will
    raise an error.

    Returns:
        AppConfig: The configuration dictionary.

    Raises:
        RuntimeError: If the configuration file does not exist or cannot be read.
    """
    config_file = CONFIG_DIR / "config.toml"

    if not config_file.exists():
        message = make_error(ErrorCode.SOURCE_NOT_FOUND, path=str(config_file))
        raise RuntimeError(message.message)

    try:
        with config_file.open("rb") as file:
            raw = tomllib.load(file)
    except PermissionError as exc:
        message = make_error(
            ErrorCode.PERMISSION_DENIED, path=str(config_file)
        )
        raise RuntimeError(message.message) from exc
    except OSError as exc:
        message = make_error(ErrorCode.SOURCE_NOT_FOUND, path=str(config_file))
        raise RuntimeError(message.message) from exc
    except Exception as exc:
        message = make_error(ErrorCode.UNKNOWN_ERROR, path=str(config_file))
        raise RuntimeError(message.message) from exc



# implement the call from main.py to init, read, and write config.toml...
# write test or manual test by printing the config values


# continue for size calculation for the source dirs
# write test or manual test by printing the size of the source dirs
