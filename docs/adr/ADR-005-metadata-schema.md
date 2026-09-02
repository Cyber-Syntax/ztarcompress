# ADR-005: Keep metadata separate from config

**Status:** Accepted  
**Date:** 2026-08-31  
**Author:** [Name]

## Decision

- Store backup details in a separate `metadata.json` file.
- Keep metadata as a small append-only history of backup records.
- Record: `format_version`, timestamp, archive name, SHA-512, size, source names, and status.
- Store artifact names, not absolute filesystem paths.

## Why

This keeps config as user setup and metadata as generated operational data. It is simple, portable, and easy to version.

## Consequences

- Clear separation between user config and backup history.
- Easy to add fields later with `format_version`.
- Less machine-specific metadata.

## Related

- [docs/TDD.md](docs/TDD.md)
- [docs/PRD.md](docs/PRD.md)
