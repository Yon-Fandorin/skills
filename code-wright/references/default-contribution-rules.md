# Default Contribution Rules

Use these rules only where the consuming repository is silent. Repository-scoped authorities and `.codewright.toml` override every default below.

## Comments And Documentation

- Write comments, API documentation, and test descriptions in the language selected for each surface by governing user or repository instructions and `.codewright.toml`. Use English only for a surface with no selected language. The English example below illustrates phrasing, not a language override.
- Explain intent, constraints, or invariants concretely enough to name the subject, boundary, and deciding condition. Do not label behavior with abstract qualities.
- Keep line comments short and move detailed context to maintained documentation.
- Document public APIs at the level expected by the target language and repository. Do not add comments that merely restate identifiers or syntax.
- When code moves, update documentation and tests that name its old owner or path.

Preferred:

```rust
// Resource kind and version
pub kind: KindRef,
```

Avoid:

```rust
// This field contains the resource kind and version.
pub kind: KindRef,
```

## Modules And Ownership

- Split files by responsibility, not line count or a one-file-per-function rule.
- Before placing new behavior in an existing module family, compare the responsibilities of the entry file, nearest siblings, and shared owner. Extending an approved tree does not by itself identify the right owner.
- Keep simple branching with its dispatcher when selecting among local behaviors is the shared responsibility. Extract behavior only when it has a distinct invariant, lifecycle, or owner; do not split a short branch merely for symmetry.
- Keep a helper in the smallest existing owner that expresses its responsibility; use a function, method, type, or focused module according to the target language and repository style.
- Introduce an abstraction for a demonstrated ownership or caller cost. For a shared abstraction, compare the policy or mechanics its deletion would restore in current callers with the interface and coupling it adds. Keep independently changing policies with their owners.
- Keep module entry files focused on composition, exports, and module-level documentation when the target ecosystem uses them.
- After placement is settled, expose each item only through its intended public API boundary or actual internal consumer path. Broader internal visibility is not a substitute for correcting ownership.
- Test-only fixture helpers may live under `tests/support` when they improve scenario readability or serve multiple integration scenarios.

## Declaration Order

- Order declarations by semantic group and the reader's entrypoint-to-helper flow, using the repository's conventions. Keep a feature's related operations together; avoid inserting another feature between a read/write pair.
- Group imports, contracts, implementation, and test declarations so each region has a clear role. Tests follow the local separate-file or end-of-file convention when applicable; no single language's order is universal.
- Preserve observable ordering when moving declarations or statements, including initialization, routing, enum representations, and side effects. Formatting alone does not establish a readable order.

## Readability

Review changed code in context, following repository conventions.

- Let the formatter handle indentation and wrapping. Use blank lines sparingly between logical steps; keep related statements together.
- Use names that reveal purpose, with units where ambiguity matters. Name dense expressions when that reduces rereading; do not add intermediates or helpers solely to shorten code.
- Make the normal path easy to trace; use guard clauses when they clarify branching. Preserve short-circuiting, evaluation count/order, cleanup, and errors in any readability refactor.
- Group related fields when order is unconstrained. Preserve positional interfaces, initialization dependencies, and observable validation, schema, or serialization order.

Keep corrections within scope. A readability finding needs a concrete reader difficulty and the smallest useful correction; treat preference-only suggestions as optional.

References: [PEP 8](https://peps.python.org/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds), [Prettier rationale](https://prettier.io/docs/rationale#empty-lines), [Google code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html#complexity).

## Verification

Use the repository-pinned toolchain and repository-provided gates when present. When the repository is silent, run the formatter or style check, compile or static check, and nearest meaningful tests that are conventional for the changed language and target. Do not introduce a new toolchain or project-wide gate merely to verify a scoped change.

Add the nearest compiler or linter command when the repository requires warning-free code or when the changed target is not compiled by those tests.
