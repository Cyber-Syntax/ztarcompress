# ADR-006: Keep encryption separate from backup

**Status:** In Review
**Date:** 2026-08-31  
**Author:** [Name]

## research

- <https://datatracker.ietf.org/doc/html/rfc9106.html#name-argon2-algorithm>
- <https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/>

## Decision

- Backup creates the archive.
- `encrypt` only encrypts an existing archive.
- `decrypt` only decrypts an encrypted archive.
- Use a mature Python crypto library, not custom crypto code.
- Store the encrypted SHA-512 in metadata.

## Why

This keeps the commands simple and reduces the chance of mixing archive creation with encryption logic.

## Consequences

- Cleaner architecture.
- Easier testing and failure handling.
- The encrypted format is simple but not the most advanced possible design.

## Related

- [docs/TDD.md](docs/TDD.md)
- [docs/PRD.md](docs/PRD.md)
