# Code Placement Review

Review the requested change's file ownership and declaration order as separate
questions. Use the consuming repository's authorities and nearest comparable
implementation, not a prescribed directory tree.

## Placement Evidence

For each substantial changed responsibility, trace the entry point, consumers,
existing owner, and closest analogous feature. Read the enclosing declarations
and neighboring implementations before selecting a location. File names and a
successful import are clues, not ownership evidence.

When placement is ambiguous, compare candidate owners by their current
responsibilities, independent change axes, and dependency direction. Finish when
the chosen owner has a concrete reason and the alternatives have a concrete cost.
For a small change, state that reason directly rather than generating a design
document or an exhaustive tree.

## Boundary Cases

- **Atomic workflows:** Trace transaction, lock, retry, resource lifetime, and
  rollback ownership before splitting orchestration. A narrow cross-domain call
  inside an existing persistence transaction may be correct; preserve the atomic
  contract instead of moving it into a separately committed operation to satisfy
  a layer diagram.
- **Multiple runtimes:** Trace server/browser/native or host/guest import paths.
  Check each real consumer of a shared helper for runtime-only dependencies and
  authentication, decoding, cancellation, or error obligations before relocating
  it. Reach the language-specific reference for representation choices.
- **Shared contracts:** Find the payload's owning public entrypoint and every
  consumer before moving a schema or type. Update actual imports rather than
  adding a compatibility export to conceal an incorrect owner.
- **Tests and fixtures:** Follow the behavior and production owner they exercise.
  A fixture with real consumers in several test modules may justify shared support;
  keep test-only access scoped to tests. Inspect consumers before extracting or
  moving their setup.

## Reading Flow

Apply the baseline's [Declaration Order](default-contribution-rules.md#declaration-order)
rules to the whole changed region, including the declaration immediately before
and after it. Inspect imports, types/schemas/conversions, related operations,
helpers, and tests; a correct directory does not settle this pass. Keep local
conventions when they provide a clear reading flow.

## Review Result

Separate required corrections from optional tidying. Each placement or order
finding needs an exact location, evidence from an owner or local precedent, the
maintenance or behavior consequence, and the smallest useful adjustment. A
different structure or shorter file alone is not a finding.

When no finding survives, state the ownership and order verdict with the relevant
rationale. Report only checks actually run; a green formatter or compiler does
not prove ownership or live integration behavior.
