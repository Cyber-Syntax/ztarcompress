# ztarcompress Roadmap

This roadmap covers the MVP from the first alpha release through
`v1.0.0` stable. Features after `v1.0.0` are listed separately.

## MVP Scope

The MVP includes:

- Linux support only
- Python 3.14+
- `backup`, `verify`, `extract`, `encrypt`, and `decrypt` commands
- TAR + Zstandard archives
- SHA-512 integrity hashes
- Safe extraction without silent overwrites
- Symlink preservation without following symlinks
- Hardlink preservation where supported
- Glob-based exclusions
- Atomic artifact and metadata writes
- Structured errors and warnings
- JSON output for automation
- Unit, integration, and failure tests

The MVP does not include cloud storage, scheduling, incremental backups,
deduplication, GUI support, or deep/full verification.

## Release Milestones

| Version | Stage | Goal |
| --- | --- | --- |
| `v0.1.0-alpha` | Foundation | Establish project structure and domain contracts |
| `v0.2.0-alpha` | Configuration | Load and validate user configuration |
| `v0.3.0-alpha` | Filesystem | Discover sources, exclusions, and size information |
| `v0.4.0-alpha` | Archive | Create TAR + Zstandard archives |
| `v0.5.0-beta` | Metadata and verification | Track artifacts and verify archive integrity |
| `v0.6.0-beta` | Extraction | Restore archives safely |
| `v0.7.0-beta` | Encryption | Encrypt and decrypt existing archives |
| `v0.8.0-beta` | CLI and integration | Complete command workflows and automation support |
| `v0.9.0-rc` | Hardening | Stabilize behavior, documentation, and release quality |
| `v1.0.0` | Stable | Ship the complete MVP |

## `v0.1.0-alpha` - Foundation

- [ ] Confirm the package layout and CLI entry point.
- [x] Establish the `src/ztarcompress` module structure.
- [ ] Add the initial CLI command dispatcher.
- [x] Define domain models, result objects, enums, and error codes.
- [x] Define structured application messages and warning messages.
- [ ] Add logging configuration without password exposure.
- [ ] Add baseline pytest fixtures.
- [ ] Add Ruff, mypy, coverage, and security checks to development workflow.
- [ ] Document Linux and Python 3.14 requirements.
- [ ] Decide whether the proposed Pydantic configuration ADR is accepted.
- [ ] Resolve the archive root-layout wording:
  follow ADR-002 and preserve real source directory names without synthetic
  `source-001/` wrappers.

Exit criteria:

- CLI starts successfully.
- Tests, linting, type checking, and coverage commands run.
- Invalid operations produce structured errors rather than scattered exits.

## `v0.2.0-alpha` - Configuration

- [ ] Implement TOML configuration loading.
- [ ] Implement the `AppConfig` validation model.
- [ ] Validate configuration version.
- [ ] Support default values for sources, exclusions, directories, and retention.
- [ ] Expand `~` and normalize configured paths.
- [ ] Validate list and scalar types.
- [ ] Validate non-negative retention values.
- [ ] Validate that required configuration values are present.
- [ ] Translate validation failures into stable application error codes.
- [ ] Add tests for valid configuration.
- [ ] Add tests for missing fields, invalid types, invalid retention, and malformed TOML.
- [ ] Update the example configuration documentation.

Exit criteria:

- Valid `config.toml` produces a strongly typed configuration object.
- Invalid configuration fails before filesystem or archive work begins.

## `v0.3.0-alpha` - Filesystem Discovery

- [ ] Resolve configured source paths.
- [ ] Validate source existence and readability.
- [ ] Walk source directories without following symlinks.
- [ ] Preserve symlink entries as symlinks.
- [ ] Detect hardlinks where supported.
- [ ] Identify regular files, directories, symlinks, FIFOs, devices, and other special entries.
- [ ] Skip unsupported special files with structured warnings.
- [ ] Implement glob exclusions relative to each source root.
- [ ] Apply exclusions consistently to size estimation and archiving.
- [ ] Calculate approximate source size without loading file contents into memory.
- [ ] Detect files that disappear or become unreadable during discovery.
- [ ] Add best-effort source-drift warnings.
- [ ] Add tests for symlinks, hardlinks, exclusions, special files, unusual filenames, and source errors.

Exit criteria:

- Source discovery returns a deterministic, archive-ready entry stream.
- Excluded paths are absent from both size estimates and archive input.

## `v0.4.0-alpha` - Archive Creation

- [ ] Implement TAR + Zstandard archive creation using Python 3.14 `tarfile`.
- [ ] Use GNU TAR format.
- [ ] Preserve real source directory names according to ADR-002.
- [ ] Preserve regular files and directories.
- [ ] Preserve symlinks without dereferencing them.
- [ ] Preserve hardlinks where supported.
- [ ] Skip FIFOs and unsupported special files with warnings.
- [ ] Stream archive data where practical.
- [ ] Write to a temporary `.tar.zst.tmp` file.
- [ ] Ensure failed archive creation does not publish a final artifact.
- [ ] Detect unreadable or disappearing source files during creation.
- [ ] Add archive creation unit and integration tests.
- [ ] Test spaces, Unicode names, empty directories, links, and large files.

Exit criteria:

- A valid `.tar.zst` archive can be created from configured sources.
- Archive creation fails instead of publishing a partial archive.

## `v0.5.0-beta` - Metadata and Verification

- [ ] Implement SHA-512 hashing for archive artifacts.
- [ ] Implement `metadata.json` loading and validation.
- [ ] Store artifact names instead of absolute paths.
- [ ] Store format version, timestamp, archive name, hash, size, sources, and status.
- [ ] Append new records without destroying existing history.
- [ ] Enforce configurable metadata retention.
- [ ] Write metadata through a temporary file and atomic replacement.
- [ ] Implement archive readability checks.
- [ ] Implement the `verify` command.
- [ ] Compare the stored SHA-512 with the current archive hash.
- [ ] Enumerate archive members during verification.
- [ ] Return structured verification results.
- [ ] Add tests for valid archives, corrupted archives, hash mismatches, missing metadata, and invalid metadata.

Exit criteria:

- `backup -> verify` succeeds only when both hash and readability checks pass.
- Metadata is never left partially written.

## `v0.6.0-beta` - Safe Extraction

- [ ] Implement the `extract` command.
- [ ] Verify the archive before extraction.
- [ ] Reject absolute archive paths.
- [ ] Reject path traversal entries.
- [ ] Use an explicit safe extraction filter.
- [ ] Detect existing destination conflicts.
- [ ] Never silently overwrite existing files.
- [ ] Preserve supported file, directory, symlink, and hardlink metadata.
- [ ] Define behavior for unsupported special files.
- [ ] Prevent partial extraction from being reported as success.
- [ ] Add extraction tests for valid archives, traversal attempts, absolute paths, collisions, links, and permissions.

Exit criteria:

- Archives extract only into safe target paths.
- Existing files remain protected unless the user explicitly chooses a safe destination or supported overwrite behavior.

## `v0.7.0-beta` - Encryption and Decryption

- [ ] Confirm and accept the encryption ADR before implementation.
- [ ] Select and document the password-based encryption format and KDF.
- [ ] Add the mature cryptography dependency.
- [ ] Implement `encrypt` for existing `.tar.zst` files only.
- [ ] Request passwords interactively in the MVP.
- [ ] Never log or persist passwords.
- [ ] Write encrypted output atomically as `.tar.zst.enc.tmp`.
- [ ] Store encrypted artifact name, SHA-512, and size in metadata.
- [ ] Implement `decrypt` without deleting the encrypted source.
- [ ] Handle wrong passwords and corrupted encrypted artifacts clearly.
- [ ] Add tests for successful encryption, decryption, wrong passwords, corruption, and partial failures.

Exit criteria:

- Encryption and decryption are independent from backup creation.
- Original archive and encrypted artifacts are retained.
- Failed crypto operations publish no partial final artifact.

## `v0.8.0-beta` - CLI and Integration

- [ ] Complete `backup`, including size preview and confirmation.
- [ ] Support `-y/--yes` for non-interactive backup.
- [ ] Implement `--json` output for results and errors.
- [ ] Add stable exit codes.
- [ ] Connect backup creation, verification, metadata, and retention.
- [ ] Connect extraction to verification.
- [ ] Connect encryption and decryption to metadata updates.
- [ ] Add end-to-end tests for:
  - [ ] configuration to backup
  - [ ] backup to verify
  - [ ] backup to extract
  - [ ] backup to encrypt
  - [ ] encrypted archive to decrypt
- [ ] Add failure tests for source drift, corrupt archives, collisions, and partial writes.
- [ ] Verify no secrets appear in logs or JSON output.

Exit criteria:

- All MVP commands work through the CLI.
- Core workflows have integration coverage.

## `v0.9.0-rc` - Hardening

- [ ] Review all behavior against the PRD acceptance criteria.
- [ ] Review all accepted ADRs for implementation consistency.
- [ ] Resolve remaining metadata schema compatibility issues.
- [ ] Confirm Linux-only support is clearly documented.
- [ ] Test large files and large archives.
- [ ] Test unusual filenames and permission combinations.
- [ ] Test interrupted and failed operations for leftover temporary files.
- [ ] Run the complete test suite with the configured coverage threshold.
- [ ] Run Ruff, mypy, and dependency security checks.
- [ ] Review user-facing errors and warnings for clarity.
- [ ] Complete README installation and usage documentation.
- [ ] Add release notes for the MVP.

Exit criteria:

- No known P0 or P1 defects remain.
- The complete MVP workflow is reproducible on Linux with Python 3.14+.

## `v1.0.0` - Stable MVP

- [ ] Tag the first stable release.
- [ ] Publish the supported installation workflow using uv.
- [ ] Publish the final configuration example.
- [ ] Publish command reference and recovery guidance.
- [ ] Confirm archive, metadata, and encryption formats are documented.
- [ ] Confirm backward-compatibility expectations for `metadata.json`.
- [ ] Confirm all release checks pass.
- [ ] Freeze MVP behavior except for bug and security fixes.

## Post-`v1.0.0` Nice-to-Have Features

These features are intentionally outside the MVP and must not delay `v1.0.0`.

### Verification

- [ ] Add the proposed `full-verify` command.
- [ ] Decrypt encrypted archives before deep verification.
- [ ] Extract into a temporary directory.
- [ ] Compare path, type, size, and SHA-512 for selected files.
- [ ] Define behavior for missing, modified, and extra files.
- [ ] Clean temporary verification data reliably.

### Backup Features

- [ ] Add incremental or differential backups.
- [ ] Add deduplication.
- [ ] Add backup scheduling.
- [ ] Add configurable compression levels.
- [ ] Add resumable backup operations.
- [ ] Add snapshot support where the platform permits it.
- [ ] Add stronger source-change detection.

### Storage and Operations

- [ ] Add cloud or remote storage integrations.
- [ ] Add removable-disk workflows.
- [ ] Add archive rotation independent of metadata retention.
- [ ] Add configurable retention policies by age and size.
- [ ] Add backup listing and pruning commands.
- [ ] Add restore previews and dry-run extraction.

### Security

- [ ] Add non-interactive secret integration through an explicit secret manager.
- [ ] Add key rotation guidance.
- [ ] Add stronger encryption format versioning.
- [ ] Add signed metadata or authenticated backup manifests.
- [ ] Add security-focused fuzz testing for archive handling.

### Platform Support

- [ ] Evaluate macOS support.
- [ ] Evaluate Windows support.
- [ ] Add platform-specific filesystem behavior tests.
- [ ] Document cross-platform link and permission differences.

### User Experience

- [ ] Add shell completion.
- [ ] Add progress reporting for large archives.
- [ ] Add colored terminal output with a non-color mode.
- [ ] Add an optional TUI.
- [ ] Add more detailed archive inspection commands.
- [ ] Add machine-readable status and metrics output.

