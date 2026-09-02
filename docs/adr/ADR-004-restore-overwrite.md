# ADR-004: Extract is safe by default

**Status:** Accepted  
**Date:** 2026-08-31  
**Author:** [Name]

## Decision

- Never overwrite existing files silently during extract.
- Reject path traversal and absolute paths inside the archive.
- If collisions happen, fail clearly or extract into a new safe target directory.

## Why

Extract is a safety-critical action. Silent overwrite is too dangerous for personal backups.

## Consequences

- More explicit recovery workflow.
- Users may need to choose a fresh extract folder.
- Safer than destructive extract behavior.

## Related

- [docs/TDD.md](docs/TDD.md)
- [docs/PRD.md](docs/PRD.md)
