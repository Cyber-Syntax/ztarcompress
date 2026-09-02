
# ADR-002: Use the tar default root layout for configured source directories

**Status:** Accepted  
**Date:** 2026-08-31  
**Author:** [Name]  
**Links:**

- [docs/TDD.md](docs/TDD.md)
- [docs/PRD.md](docs/PRD.md)

---

## Context

The backup tool may be configured to back up multiple directories, such as:

- `~/Documents`
- `~/Projects`

The question is whether to add a synthetic internal root like `source-001/` or let the tar archive preserve the real directory names as they exist on disk.

This is a simple backup tool, and we want the default behavior to be as close as possible to normal tar usage.

---

## Decision

We will use the default tar behavior and store the real directory names as they exist in the source tree.

Example layout:

```text
Documents/
    ...
Projects/
    ...
```

If the user config includes two different directories with different names, they remain distinct in the archive without any artificial wrapper directory.

We do not add a `source-001/` or similar synthetic root by default.

---

## Alternatives Considered

| Alternative | Pros | Cons | Why Not Chosen |
| --- | --- | --- | --- |
| Synthetic source root like `source-001/` | Can enforce a strict boundary | Adds unnecessary nesting and extra complexity | Not needed for normal Linux directory names |
| Preserve real directory names | Simple, natural, and matches tar defaults | Requires care when the same directory name is used in different places | Chosen approach |
| Store absolute paths in the archive | Unique paths | Unsafe and not portable | Rejected |

---

## Consequences

### Positive Consequences

- Keeps the archive simple and close to standard tar behavior.
- Easier for junior developers to understand.
- No artificial wrapper directory to debug.

### Negative Consequences

- If users choose two different source roots with the same directory name, the archive may need a clear naming decision later.
- This is not a common case for normal Linux usage.

### Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation Strategy |
| --- | --- | --- | --- |
| Two sources share the same basename | Low | Low | This is uncommon on Linux and can be handled later if needed |
| User expects a synthetic root wrapper | Low | Low | Document that the tool uses the actual directory names by default |

---

## Related Decisions

- ADR-001: Preserve symlinks and hardlinks safely during archive creation
- ADR-003: Fail backup when a source file disappears or becomes unreadable
