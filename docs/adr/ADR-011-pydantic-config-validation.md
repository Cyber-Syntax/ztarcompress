# ADR-011: Use Pydantic for configuration validation

**Status:** Proposed  
**Date:** 2026-09-01  
**Author:** [Name]

## Decision

- Adopt Pydantic v2 as the validation layer for `AppConfig` and related configuration data.
- Replace the custom `from_mapping()` validation logic with native Pydantic parsing and field validation.
- Keep the project’s existing `ErrorCode` and `make_error()` flow at the boundary layer, but use `model_validate()` to convert TOML data into a strongly typed config object.
- Treat the config schema as the source of truth for required fields, default values, path normalization, and type enforcement.

## Context

The project currently defines `AppConfig` as a dataclass-like model with custom validation helpers in `models.py` and manual parsing in `config.py`. The validation work is split between:

- the Python dataclass defaults,
- the hand-written `from_mapping()` method,
- and the TOML loader in `read_config()`.

This creates a few problems:

- Validation logic is duplicated across multiple places.
- Type enforcement is custom and easy to drift over time.
- Path normalization and required-field checks are not expressed as a single schema.
- The config boundary is harder to reason about when new fields are added.

The project needs a maintainable configuration layer that is explicit, compact, and safe for CLI and automation use.

## Research and rationale

### Why a dedicated validation library

Configuration files are an ideal use case for a schema validator because they are:

- user-provided input,
- versioned and potentially partial,
- strongly type-sensitive,
- sensitive to path and retention semantics,
- and likely to evolve over time.

A library such as Pydantic provides a clear schema, consistent error handling, and validation features that are difficult to maintain manually without introducing bugs.

### Why Pydantic specifically

Pydantic offers several advantages that are relevant here:

- First-class type coercion and validation for Python primitives and paths.
- Built-in support for `Path`, `list[str]`, `int`, and other datatypes the project already uses.
- Clear validation hooks with `field_validator` and `model_validator` for custom constraints.
- A strong ecosystem and cross-project familiarity.
- Easy compatibility with TOML-driven configuration when the data is loaded into a dictionary and validated at the boundary.

The project is already using modern Python patterns and is not dependent on a heavy framework. Pydantic fits the project’s scale and purpose without adding architectural complexity.

## Alternatives considered

### 1. Keep the custom validation layer

Retain the dataclass + `from_mapping()` infrastructure.

Positive:

- No dependency added.
- Can be implemented incrementally.
- Keeps the current code path familiar.

Negative:

- More boilerplate and manual type checks.
- Harder to test and maintain.
- More likely to drift as config fields evolve.
- Repetitive validation logic across multiple code paths.

This option is easy to start with but becomes fragile as the config schema grows.

### 2. Use `dataclass` + custom validators only

Keep the config model as data classes and add explicit validation functions.

Positive:

- Minimal external dependency footprint.
- Full control over validation behavior.

Negative:

- Still requires writing and maintaining custom runtime checks.
- Makes error formatting less consistent.
- Less ergonomic than a formal schema layer.

This is not enough for the project’s long-term maintainability needs.

### 3. Use Pydantic for the entire app model surface

Use Pydantic not only for config, but for all core data models.

Positive:

- Consistent validation across the system.
- Strong schema semantics for config and operational metadata.

Negative:

- Broader change with more risk.
- Not necessary for the current scope.
- Could affect archival and verification code in ways that are not needed for the initial migration.

This is a potentially valid future direction, but it is broader than necessary. For this decision, the project should adopt Pydantic at the configuration boundary only.

## Positives

- Clear schema definition for `AppConfig`.
- Better validation coverage than the existing ad hoc checks.
- Smaller, more maintainable config boundary code.
- Easier extension as new config fields are introduced.
- Better error messages for invalid user configuration.
- Aligns with Python best practices for typed application configuration.

## Risks and trade-offs

### Risk: dependency footprint

Adding Pydantic introduces a new runtime dependency. For a CLI backup tool, this is usually acceptable, but it is still a project-level decision and should be documented.

Mitigation:

- Pin or constrain the supported version clearly in the project metadata.
- Keep the migration focused on config validation only.

### Risk: behavior change during migration

The current validation code may be permissive in some ways or rely on specific error patterns. Migrating to Pydantic may subtly change how invalid config values are reported.

Mitigation:

- Translate Pydantic errors into the project’s existing `RuntimeError` / `ErrorCode.INVALID_CONFIG` flow.
- Add focused tests for invalid input cases before broader rollout.

### Risk: path semantics

A config file can contain `~`, relative paths, and platform-specific path strings. Pydantic validation must normalize these carefully so the app behaves as expected.

Mitigation:

- Validate paths using `Path` conversion with `expanduser()` and explicit normalization steps.
- Keep the model’s default values and generated TOML aligned with the same semantics.

## Consequences

### Positive consequences

- `AppConfig` becomes a single source of truth for config schema and defaults.
- The parsing boundary in `read_config()` becomes simpler and easier to reason about.
- New configuration keys are easier to add correctly and safely.
- Validation failures become more structured and consistent.

### Negative consequences

- The project gains a new dependency.
- Some configuration assumptions will need to be re-expressed in Pydantic terms.
- There is a short migration cost while removing the legacy `from_mapping` logic.

## Implementation notes

This ADR does not require a large refactor across the app. The migration should stay intentionally narrow:

- Convert `AppConfig` to a Pydantic model.
- Ensure all required fields and defaults remain stable.
- Validate loaded TOML at the `read_config()` boundary.
- Keep `make_error()` and existing error codes for CLI-facing errors.
- Add tests around invalid config values, valid config values, and path expansion.

A practical migration path is:

1. Add Pydantic as a dependency.
2. Update `AppConfig` to inherit from `BaseModel`.
3. Replace `from_mapping` with `model_validate` or equivalent Pydantic construction.
4. Update config file readers to validate TOML data directly.
5. Add tests for the migration boundary.

## Related documents

- [docs/TDD.md](docs/TDD.md)
- [docs/PRD.md](docs/PRD.md)
- [src/ztarcompress/models.py](src/ztarcompress/models.py)
- [src/ztarcompress/config.py](src/ztarcompress/config.py)

## Summary

The project should adopt Pydantic for configuration validation because it provides a clear schema-driven path for user configuration, reduces custom validation maintenance, and keeps the config boundary easier to extend and reason about without broadening the app’s architectural footprint beyond what the project needs.
