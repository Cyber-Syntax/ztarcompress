# ADR-009: Full verification is a future feature

**Status:** Proposed  
**Date:** 2026-08-31  
**Author:** [Name]

## Decision

- Do not include full verification in the MVP.
- Later, add a separate `full-verify` command.
- It will decrypt when needed, extract to a temporary directory, compare regular files, and clean up afterward.

## Why

This is expensive and not needed for the first reliable backup workflow. We keep the MVP simple and add stronger checks later.

## Consequences

- Normal `verify` stays fast and practical.
- Deep verification is available later as an explicit advanced feature.

## Related

- [docs/TDD.md](docs/TDD.md)
- [docs/PRD.md](docs/PRD.md)

# 11. Be precise about what full verification compares

I would **not say "hash some files" without specifying the algorithm**.

A stronger future verification design could compare a manifest like:

```text
relative path
file type
file size
SHA-512
```

For example:

```json
{
  "path": "Documents/report.pdf",
  "type": "file",
  "size": 58291,
  "sha512": "..."
}
```

Then:

```text
source file
     ↓
SHA-512
     ↓
compare
     ↑
extracted file
```

This is much stronger than merely saying:

> "The file exists."

But you don't necessarily need to generate a manifest for **every source file during ordinary backup**. That could significantly increase work and complexity.

I'd therefore make this a feature of:

```text
full-verify
```

rather than MVP normal verification.

---

Then the later high-confidence operation:

```text
             FULL VERIFY
                  │
                  ▼
        decrypt if necessary
                  │
                  ▼
         verify archive/hash
                  │
                  ▼
        temporary extraction
                  │
                  ▼
       compare files + hashes
                  │
                  ▼
             final result
```
