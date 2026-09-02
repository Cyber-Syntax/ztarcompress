# ADR-003: Fail the backup on source drift

**Status:** Accepted  
**Date:** 2026-08-31  
**Author:** [Name]

## Decision

- Warn that files may change during backup.
- If a source file disappears or becomes unreadable during archive creation, fail the backup.
- Do not publish a partial archive or report success.

## Why

This is safer than partial backup success. For important documents and config files, false success is worse than a failed backup.

## Consequences

- Backups may fail if the source files are actively changing.
- Users need to close editors or browsers before running a backup when possible.

## Related

- [docs/TDD.md](docs/TDD.md)
- [docs/PRD.md](docs/PRD.md)
