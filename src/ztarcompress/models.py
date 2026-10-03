"""Domain models for ztarcompress.

This module contains the core dataclasses and enums used throughout the CLI.
The models are intentionally narrow and focused on the backup domain: user
configuration, source discovery, archive lifecycle, verification, extraction,
and structured operational messaging.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Mapping
    from datetime import datetime


@dataclass
class AppConfig:
    """Configuration loaded from the user's config.toml file.

    Args:
        config_version: Version of the configuration schema
        sources: Ordered list of configured source directories.
            (default: ~/Documents, ~/.config)
        exclude: Glob-style exclusion patterns to ignore during backup.
            (default: **/node_modules, **/.venv, **/__pycache__, **/.ruff_cache)
        backup_directory: Directory where archive files should be written.
            (default: ~/.local/share/ztarcompress/backups)
        config_directory: Directory where the config.toml file is located.
            (default: ~/.config/ztarcompress)
        log_directory: Directory where log files should be written.
            (default: ~/.local/state/ztarcompress/logs)
        cache_directory: Directory where cache files should be written.
            (default: ~/.cache/ztarcompress)
        metadata_retention: Maximum number of metadata records to retain.
            (default: 10)
        archive_retention: Retained max number of archive files.
            (default: 2)
        encrypted_archive_retention: Retained max number of encrypted archive.
            (default: 1)
        decrypted_archive_retention: Retained max number of decrypted archive.
            (default: 1)
        extracted_archive_retention: Retained max number of extracted archive.
            (default: 1)
    """

    config_version: int = 1
    sources: list[str] = field(
        default_factory=lambda: ["~/Documents", "~/.config"]
    )
    exclude: list[str] = field(
        default_factory=lambda: [
            "**/node_modules",
            "**/.venv",
            "**/__pycache__",
            "**/.ruff_cache",
        ]
    )
    backup_directory: Path = (
        Path.home() / ".local" / "share" / "ztarcompress" / "backups"
    )
    config_directory: Path = Path.home() / ".config" / "ztarcompress"
    log_directory: Path = (
        Path.home() / ".local" / "state" / "ztarcompress" / "logs"
    )
    cache_directory: Path = Path.home() / ".cache" / "ztarcompress"
    metadata_retention: int = 10
    archive_retention: int = 2
    encrypted_archive_retention: int = 1
    decrypted_archive_retention: int = 1
    extracted_archive_retention: int = 1

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> AppConfig:
        """Create an AppConfig instance from a raw mapping.

        Args:
            cls: The AppConfig class itself.
            raw: A dictionary-like object containing configuration values.

        Returns:
            An instance of AppConfig populated with values from the mapping.
        """
        if not isinstance(raw, dict):
            message = make_error(
                ErrorCode.INVALID_CONFIG,
                reason="Expected a dictionary-like object.",
            )
            raise TypeError(message.message)

        # TODO: add the helper make_error func
        # validate these are the correct way to validate the config types???
        def require_int(key: str) -> int:
            value = raw.get(key)
            if not isinstance(value, int):
                message = make_error(
                    ErrorCode.INVALID_CONFIG,
                    path=str(key),
                    reason=f"'{key}' must be an integer.",
                )
                raise TypeError(message.message)
            return value

        def require_list_of_strings(key: str) -> list[str]:
            value = raw.get(key)
            if not isinstance(value, list) or not all(
                isinstance(item, str) for item in value
            ):
                message = make_error(
                    ErrorCode.INVALID_CONFIG,
                    path=str(key),
                    reason=f"'{key}' must be a list of strings.",
                )
                raise TypeError(message.message)
            return value

        def require_path(key: str) -> Path:
            value = raw.get(key)
            if not isinstance(value, str):
                message = make_error(
                    ErrorCode.INVALID_CONFIG,
                    path=str(key),
                    reason=f"'{key}' must be a string representing a path.",
                )
                raise TypeError(message.message)
            return Path(value).expanduser().resolve()

        return cls(
            config_version=require_int("config_version"),
            sources=require_list_of_strings("sources"),
            exclude=require_list_of_strings("exclude"),
            backup_directory=require_path("backup_directory"),
            config_directory=require_path("config_directory"),
            log_directory=require_path("log_directory"),
            cache_directory=require_path("cache_directory"),
            metadata_retention=require_int("metadata_retention"),
            archive_retention=require_int("archive_retention"),
            encrypted_archive_retention=require_int(
                "encrypted_archive_retention"
            ),
            decrypted_archive_retention=require_int(
                "decrypted_archive_retention"
            ),
            extracted_archive_retention=require_int(
                "extracted_archive_retention"
            ),
        )


@dataclass
class BackupSource:
    """One source directory after path expansion and validation.

    Args:
        path: Resolved filesystem path for the directory to back up.
        display_name: User-facing label for the source root.
        exclude_patterns: Exclusion patterns applied relative to this root.
        is_valid: True when the source directory is usable for backup.
    """

    path: Path
    display_name: str
    exclude_patterns: list[str] = field(default_factory=list)
    is_valid: bool = True


@dataclass
class BackupPlan:
    """The computed archive workload before the actual backup is written.

    Args:
        source_roots: Source directories included in the plan.
        candidate_files: Files selected to be stored in the archive.
        estimated_size_bytes: Approximate total payload size.
        needs_confirmation: Whether the user should confirm before writing.
    """

    source_roots: list[BackupSource] = field(default_factory=list)
    candidate_files: list[Path] = field(default_factory=list)
    estimated_size_bytes: int = 0
    needs_confirmation: bool = True


class BackupStatus(Enum):
    """Lifecycle state for a backup archive or derived output.

    These values describe where a file sits in the backup workflow: planned,
    created, verified, extracted, encrypted, decrypted, or failed.
    """

    PLANNED = auto()
    READY = auto()
    ARCHIVED = auto()
    VERIFIED = auto()
    EXTRACTED = auto()
    ENCRYPTED = auto()
    DECRYPTED = auto()
    FAILED = auto()
    PARTIAL = auto()


@dataclass
class ArchiveFile:
    """A generated backup archive created by the application.

    Args:
        path: Filesystem location of the archive.
        filename: Archive file name only.
        created_at: Timestamp of archive creation.
        size_bytes: Archive size in bytes.
        sha512: SHA-512 digest for the archive contents.
        status: Current lifecycle state for the archive.
    """

    path: Path
    filename: str
    created_at: datetime
    size_bytes: int = 0
    sha512: str = ""
    status: BackupStatus = BackupStatus.PLANNED


@dataclass
class BackupMetadata:
    """Database-like metadata record for a single archive in metadata.json.

    Args:
        schema_version: Metadata schema version, separate from application version.
        archive_name: Filename of the archive.
        archive_path: Path to the archive on disk.
        sha512: SHA-512 digest of the archive.
        size_bytes: Archive size in bytes.
        created_at: Time the record was created.
        status: State of the archive when this metadata record was saved.
        sources: Source roots included in that archive.
    """

    schema_version: int = 1
    archive_name: str = ""
    archive_path: str = ""
    sha512: str = ""
    size_bytes: int = 0
    created_at: datetime | None = None
    status: BackupStatus = BackupStatus.ARCHIVED
    sources: list[str] = field(default_factory=list)


@dataclass
class VerificationResult:
    """Result of verifying an archive's integrity and readability.

    Args:
        hash_ok: Whether the computed SHA-512 matches the recorded value.
        archive_readable: Whether the archive can be opened successfully.
        member_scan_ok: Whether archive members can be enumerated without error
        warnings: Non-fatal conditions encountered during verification.
        errors: Fatal issues that prevent successful verification.
    """

    hash_ok: bool = False
    archive_readable: bool = False
    member_scan_ok: bool = False
    warnings: list[AppMessage] = field(default_factory=list)
    errors: list[AppMessage] = field(default_factory=list)


@dataclass
class ExtractionTarget:
    """Target directory configuration for safe archive extraction.

    Args:
        destination: Directory where archive contents will be restored.
        allow_overwrite: Whether overwrite is allowed during extraction.
        strict_mode: Whether unsafe member paths should be rejected.
    """

    destination: Path
    allow_overwrite: bool = False
    strict_mode: bool = True


@dataclass
class EncryptionResult:
    """Outcome of encrypting or decrypting an archive.

    Args:
        input_path: Source archive passed to the encryption workflow.
        output_path: Generated encrypted or decrypted output file.
        sha512: SHA-512 digest of the output file.
        status: Current lifecycle state of the output file.
    """

    input_path: Path
    output_path: Path
    sha512: str = ""
    status: BackupStatus = BackupStatus.READY


class ResultCode(Enum):
    """Stable machine-readable identifiers for successful or informational results."""

    ARCHIVE_CREATED = auto()
    ARCHIVE_VERIFIED = auto()
    ARCHIVE_EXTRACTED = auto()
    ARCHIVE_ENCRYPTED = auto()
    ARCHIVE_DECRYPTED = auto()


@dataclass
class AppMessage:
    """Structured warning, error, or result message for CLI and automation consumers.

    Args:
        code: Stable identifier for the message category.
        message: Human-readable summary of the issue or state change.
        details: Optional machine-readable metadata for debugging or JSON output.
    """

    code: ErrorCode | WarningCode | ResultCode
    message: str
    details: dict[str, str] = field(default_factory=dict)


class ErrorCode(Enum):
    """Stable machine-readable identifiers for operational failures.

    These codes represent conditions that can compromise archive integrity,
    prevent a required operation, or block the application from continuing.
    """

    UNKNOWN_ERROR = auto()
    PERMISSION_DENIED = auto()
    SOURCE_NOT_FOUND = auto()
    INVALID_CONFIG = auto()
    HASH_MISMATCH = auto()
    ARCHIVE_CORRUPT = auto()
    ARCHIVE_READ_ERROR = auto()
    EXTRACTION_BLOCKED = auto()
    ENCRYPTION_FAILED = auto()
    DECRYPTION_FAILED = auto()


class WarningCode(Enum):
    """Stable machine-readable identifiers for non-fatal warnings.

    Warnings should not stop the application or invalidate archive integrity.
    They usually describe best-effort metadata collection or transient state
    changes that do not prevent successful archival or extraction.
    """

    FILE_CHANGED_DURING_BACKUP = auto()
    FILE_CHANGED_DURING_SIZE_CALC = auto()


ERROR_MESSAGES: dict[ErrorCode, str] = {
    ErrorCode.UNKNOWN_ERROR: "An unknown error occurred during the operation.",
    ErrorCode.PERMISSION_DENIED: "Permission denied while accessing a file or directory.",
    ErrorCode.SOURCE_NOT_FOUND: "Source directory does not exist or is not readable.",
    ErrorCode.INVALID_CONFIG: "Configuration is invalid or missing required values.",
    ErrorCode.HASH_MISMATCH: "Archive hash does not match the expected SHA-512 value.",
    ErrorCode.ARCHIVE_CORRUPT: "Archive is corrupted or unreadable.",
    ErrorCode.ARCHIVE_READ_ERROR: "Archive could not be opened for verification.",
    ErrorCode.EXTRACTION_BLOCKED: "Extraction blocked because a member path is unsafe.",
    ErrorCode.ENCRYPTION_FAILED: "Encryption failed while processing the archive.",
    ErrorCode.DECRYPTION_FAILED: "Decryption failed because the password is wrong or the content is invalid.",
}

WARNING_MESSAGES: dict[WarningCode, str] = {
    WarningCode.FILE_CHANGED_DURING_BACKUP: "A source file changed while being backed up; snapshot consistency is best effort only.",
    WarningCode.FILE_CHANGED_DURING_SIZE_CALC: "A source file changed while calculating size; archive contents may have shifted during planning.",
}

RESULT_MESSAGES: dict[ResultCode, str] = {
    ResultCode.ARCHIVE_CREATED: "Archive created successfully.",
    ResultCode.ARCHIVE_VERIFIED: "Archive verification passed.",
    ResultCode.ARCHIVE_EXTRACTED: "Archive extracted successfully.",
    ResultCode.ARCHIVE_ENCRYPTED: "Archive encrypted successfully.",
    ResultCode.ARCHIVE_DECRYPTED: "Archive decrypted successfully.",
}


def make_error(code: ErrorCode, **details: str) -> AppMessage:
    """Create a known error message from the centralized error catalog.

    Args:
        code: The error code to look up in the catalog.
        details: Optional key-value pairs providing additional context.

    Returns:
        An AppMessage instance containing the error code, message, and details.
    """

    return AppMessage(
        code=code, message=ERROR_MESSAGES[code], details=dict(details)
    )


def make_warning(code: WarningCode, **details: str) -> AppMessage:
    """Create a known warning message from the centralized warning catalog.

    Args:
        code: The warning code to look up in the catalog.
        details: Optional key-value pairs providing additional context.

    Returns:
        An AppMessage instance containing the warning code, message, and details.
    """

    return AppMessage(
        code=code, message=WARNING_MESSAGES[code], details=dict(details)
    )


def make_result(code: ResultCode, **details: str) -> AppMessage:
    """Create a known info message from the centralized result catalog.

    Args:
        code: The result code to look up in the catalog.
        details: Optional key-value pairs providing additional context.

    Returns:
        An AppMessage instance containing the result code, message, and details.
    """

    return AppMessage(
        code=code, message=RESULT_MESSAGES[code], details=dict(details)
    )


__all__ = [
    "ERROR_MESSAGES",
    "RESULT_MESSAGES",
    "WARNING_MESSAGES",
    "AppMessage",
    "ArchiveFile",
    "BackupConfig",
    "BackupMetadata",
    "BackupPlan",
    "BackupSource",
    "BackupStatus",
    "EncryptionResult",
    "ErrorCode",
    "ExtractionTarget",
    "ResultCode",
    "VerificationResult",
    "WarningCode",
    "make_error",
    "make_result",
    "make_warning",
]
