# Product Requirements Document (PRD)

**Project:** ztarcompress  
**Status:** Draft  
**Date:** 2026-08-31

---

## 1. Overview

ztarcompress is a Python CLI for creating safe, verifiable backup archives from user-selected directories. The MVP focuses on a reliable unencrypted backup flow, with separate commands for verification, extraction, encryption, and decryption.

The product must prioritize:

- correctness over feature breadth,
- explicit failure handling,
- safe extraction and verification,
- simple command responsibilities,
- maintainability for a junior-to-intermediate developer.

## 2. Goals

- Back up configured source directories into TAR + Zstandard archives.
- Support `config.toml` for source directories, exclusion rules, backup directory, and retention settings.
- Estimate size before backup and ask for confirmation unless `-y/--yes` is supplied.
- Preserve ordinary files/directories and keep symlinks/hardlinks safe.
- Exclude noisy paths like `node_modules`, `.venv`, `__pycache__`, and `.ruff_cache`.
- Compute and store SHA-512 hashes for archive and encrypted artifacts.
- Keep backup history in a separate `metadata.json` file.
- Verify the archive before reporting success.
- Extract archives safely without silent overwrite or path traversal.
- Provide independent commands for `backup`, `verify`, `extract`, `encrypt`, and `decrypt`.
- Keep the MVP limited to a reliable Linux workflow.

## 3. Non-Goals

- No cloud storage or remote sync.
- No incremental or differential backup model.
- No deduplication.
- No custom archive format replacing tar.
- No snapshot guarantee while files are actively changing.
- No password rotation or advanced key-management system in the MVP.
- No full deep verification in the MVP; that remains a future feature.
- No support for every special filesystem object in an identical cross-platform way.

## 4. User Stories

### US-001: Configure sources

As a user, I want to define source directories in `config.toml` so I do not have to enter them for every backup.

Acceptance criteria:

- Multiple sources are supported.
- `~` expansion works.
- Missing or invalid sources fail clearly.

### US-002: Configure exclusions

As a user, I want exclusion rules so large unnecessary directories are not archived.

Acceptance criteria:

- Exclusions are configurable.
- Matching paths are skipped before archive creation.

### US-003: Preview backup size

As a user, I want to see the size before backup so I can confirm the operation.

Acceptance criteria:

- Total size is calculated before archive creation.
- The interactive flow asks for confirmation.
- `-y/--yes` bypasses confirmation for automation.

### US-004: Create backup

As a user, I want a valid archive artifact created from my configured directories.

Acceptance criteria:

- A `.tar.zst` archive is produced.
- The archive is readable and valid.
- Ordinary files/directories are preserved.

### US-005: Verify backup

As a user, I want archive verification before success is reported.

Acceptance criteria:

- SHA-512 is checked against metadata.
- The archive is opened and enumerated to confirm readability.

### US-006: Extract backup

As a user, I want to extract a valid backup into a target directory.

Acceptance criteria:

- Extraction is safe.
- Dangerous paths are rejected.
- Existing files are not silently overwritten.

### US-007: Maintain metadata

As a user, I want backup history in one metadata file so I can inspect previous backups.

Acceptance criteria:

- `metadata.json` stores multiple records.
- Records include artifact names, hashes, sizes, and status.
- Retention defaults to 10 records.

### US-008: Encrypt existing archive

As a user, I want encryption to be a separate command so it is not mixed into backup creation.

Acceptance criteria:

- `encrypt` accepts an existing `.tar.zst`.
- Output is a new `.tar.zst.enc` file.
- SHA-512 is recorded for the encrypted artifact.

### US-009: Decrypt encrypted archive

As a user, I want to decrypt without affecting the original encrypted file.

Acceptance criteria:

- `decrypt` creates a new decrypted artifact.
- Wrong password or corruption fails clearly.

### US-010: Handle changing files

As a user, I want clear warnings when source files change during backup.

Acceptance criteria:

- The tool warns that snapshot consistency is best effort.
- The tool does not claim perfect filesystem consistency.

## 5. Functional Requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| FR-001 | Load and validate `config.toml` | P0 |
| FR-002 | Support multiple configured source directories | P0 |
| FR-003 | Expand user paths such as `~` | P0 |
| FR-004 | Support configurable exclusions | P0 |
| FR-005 | Calculate source size before backup | P0 |
| FR-006 | Support `-y/--yes` confirmation bypass | P0 |
| FR-007 | Create TAR + Zstandard archives | P0 |
| FR-008 | Preserve ordinary file and directory structure | P0 |
| FR-009 | Preserve symlinks without blindly following them | P0 |
| FR-010 | Preserve hardlinks where supported | P1 |
| FR-011 | Skip FIFOs in the MVP | P0 |
| FR-012 | Handle unusual filenames | P0 |
| FR-013 | Calculate SHA-512 for archive files | P0 |
| FR-014 | Store multiple backup records in `metadata.json` | P0 |
| FR-015 | Keep 10 metadata records by default | P0 |
| FR-016 | Make metadata retention configurable | P1 |
| FR-017 | Verify archive hash and readability | P0 |
| FR-018 | Publish files atomically | P0 |
| FR-019 | Extract archives safely | P0 |
| FR-020 | Separate `backup`, `verify`, `extract`, `encrypt`, and `decrypt` commands | P0 |
| FR-021 | Encrypt existing `.tar.zst` files | P1 |
| FR-022 | Store encrypted SHA-512 | P1 |
| FR-023 | Decrypt `.tar.zst.enc` files | P1 |
| FR-024 | Handle encryption/decryption errors safely | P1 |
| FR-025 | Keep deep verification as a future feature | P2 |
| FR-026 | Emit structured warnings and errors | P0 |
| FR-027 | Provide unit tests | P0 |
| FR-028 | Provide integration tests | P0 |
| FR-029 | Retain original artifacts when creating derived ones | P0 |
| FR-030 | Use timestamped artifact names | P0 |

## 6. Non-Functional Requirements

- Performance: Stream large files where practical; avoid loading file contents fully into memory.
- Reliability: Do not report success after a failed verification step.
- Atomicity: Final artifacts and metadata updates must be atomic.
- Security: Never log passwords; use a mature cryptography library.
- Integrity: SHA-512 is the single project hash.
- Safety: Prevent path traversal and absolute path writes during extraction.
- Maintainability: Favor small, single-responsibility functions and simple control flow.
- Python: Use Python 3.14+.
- Observability: Use logging for diagnostics without exposing secrets.
- Portability: Keep OS assumptions minimal and document Linux-specific behavior as part of the MVP.

## 7. Scope & Assumptions

### In scope

- Python CLI backup tool
- `config.toml` handling
- TAR + Zstandard archive creation
- Safe extraction
- SHA-512 verification
- Metadata bookkeeping
- Optional encryption/decryption layer
- Unit and integration tests

### Out of scope

- Cloud sync or remote backup storage
- Incremental/differential backups
- Deduplication
- Scheduling
- GUI
- Automatic key rotation

### Assumptions

- Users can read configured source directories.
- Files may change while being backed up; warnings are required.
- The backup destination is writable and has enough space.
- The project supports Linux as the first official release target.

## 8. Open Questions

| Question | Owner | Status | Resolution |
| --- | --- | --- | --- |
| What exact exclusion semantics should `config.toml` support? | Project | Open | Before filesystem implementation |
| What exact collision policy should extraction use if files already exist? | Project | Open | Before extraction implementation |
| What exact encryption format and KDF should be used? | Project | Open | Before encryption implementation |
| What exact metadata fields are required for long-term compatibility? | Project | Open | Before metadata finalization |
| What platforms will be officially supported beyond Linux? | Project | Open | Before release |

---
