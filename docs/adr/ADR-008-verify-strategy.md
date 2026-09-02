# ADR-008: Verify uses hash plus archive readability

**Status:** Accepted  
**Date:** 2026-08-31  
**Author:** [Name]

## Decision

- `verify` compares the stored SHA-512 with the current archive file.
- It also opens the archive and enumerates members to confirm the tar archive is readable.
- This is the normal verification path for the MVP.

## Why

Hash-only verification is too weak. Archive readability check adds a second safety layer without making normal verify too expensive.

## Consequences

- Good speed/safety balance.
- More reliable than hash-only verification.
- Deep extraction comparison stays separate for later.

## Related

- [docs/TDD.md](docs/TDD.md)
- [docs/PRD.md](docs/PRD.md)
