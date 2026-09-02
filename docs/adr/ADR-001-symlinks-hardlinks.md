# ADR-001: Preserve symlinks and hardlinks safely

**Status:** Accepted  
**Date:** 2026-08-31  
**Author:** [Name]

## Decision

- Preserve symlinks as symlinks.
- Do not follow symlinks while scanning source directories.
- Preserve hardlinks where the tar implementation supports them.
- Skip unsupported special files such as FIFOs with a warning.

## Why

This is the safest simple rule for a backup tool. It avoids accidentally backing up data outside the intended source tree and keeps the archive faithful to the source filesystem.

## Consequences

- Safer than following symlinks.
- Simpler to explain and test.
- Some links may not be expanded into regular files during extract.

## Related

- [docs/TDD.md](docs/TDD.md)
- [docs/PRD.md](docs/PRD.md)
