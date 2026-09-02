# ADR-007: Use simple glob exclusions

**Status:** Accepted  
**Date:** 2026-08-31  
**Author:** [Name]

## Decision

- Use glob-style patterns in `config.toml`.
- Match them relative to each source root.
- Skip matches such as `**/node_modules`, `**/.venv`, `**/__pycache__`, and `**/.ruff_cache`.

## Why

This is simple, readable, and enough for the MVP. It keeps backup size under control without introducing a complex rule system.

## Consequences

- Clear config format.
- Smaller backups.
- Not as complete as full `.gitignore` semantics.

## Related

- [docs/TDD.md](docs/TDD.md)
- [docs/PRD.md](docs/PRD.md)
