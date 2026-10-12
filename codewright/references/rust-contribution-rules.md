# Rust Contribution Rules

Read this reference only when the changed target is Rust. Repository authorities override every rule below.

## Documentation And Tests

- Use concise noun or phrase forms for field and variant documentation when that matches the repository's established rustdoc style.
- Document public modules, types, fields, variants, functions, and associated methods unless the repository deliberately uses a different public-documentation policy.
- Re-audit public documentation whenever Rust code moves or splits across files.
- When the repository uses situation/result comments above tests, place them immediately above the test's complete attribute block and avoid repeating the function name.

## Type Layout

- When fields or variants have rustdoc comments, follow the repository's blank-line convention; if none exists, separate documented members for readability.
- Order fields, variants, and associated methods by semantic group and domain or operation flow, not mechanically by name or type.
- Preserve that member order in constructors, destructuring patterns, and match arms when practical.

## Modules And Ownership

- Prefer a directory module when a concept already has multiple responsibilities; do not create one only because it might grow.
- For a new or deliberately reorganized module tree, prefer `foo.rs` with children under `foo/`. An existing `foo/mod.rs` may remain when it is outside the change or deliberately required by repository convention.
- For a new or deliberately reorganized source unit-test namespace that needs private access, use the owning module's `tests/mod.rs`. Declare `#[cfg(test)] mod tests;` after production declarations and re-exports. This does not apply to Cargo integration-test helpers: nested helpers such as `tests/common/mod.rs` avoid direct integration-target discovery and remain appropriate.
- Keep module entry files focused on module documentation, declarations, and deliberate re-exports regardless of which supported file layout owns the entry.
- Put private behavior on an owning type when that owner is clear. Keep a free function when it is the idiomatic local helper or the intentional API.
- Review the parent module and every real call site before choosing `pub(super)`, `pub(in ...)`, or `pub(crate)`; use the narrowest scope that follows the actual module route.

## Verification

- When maintaining the bundled private-unit and public-integration test-layout fixture, or auditing that fixture after a toolchain change, run the [skill-local test-layout validator](../scripts/validate_rust_test_layout.sh). Do not run it for ordinary Rust work.

Use the repository-pinned toolchain and gates. For a Rust workspace with no stricter local command, run:

```text
cargo fmt --all -- --check
cargo test --workspace
```

When `rust-toolchain.toml` pins nightly or the repository explicitly requires it, invoke the formatter with `cargo +nightly fmt --all -- --check`. Do not introduce a nightly requirement into a repository that has not chosen one.
