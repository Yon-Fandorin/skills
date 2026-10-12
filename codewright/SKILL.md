---
name: codewright
description: >-
  Implement, refactor, and review scoped code changes under the repository's
  contribution rules and optional Codewright profile. Use when code, tests, or
  module placement must change, or an existing change needs placement and
  readability review, or the user asks to configure Codewright for a repository.
  Not for architecture-only planning or
  whole-codebase quality audits.
---

# Codewright

Turn approved behavior into the smallest repository-native change, or review that change within the requested scope.

## Sources

Read applicable sources in this order. Earlier sources override later ones; the baseline always supplies unresolved defaults:

1. the user's current request and approved decisions;
2. repository authorities such as scoped `AGENTS.md` and `CONTRIBUTING.md` files;
3. the repository-root `.codewright.toml` profile for language and shape-approval settings;
4. a task-specific reference whose pointer below matches the work;
5. [references/default-contribution-rules.md](references/default-contribution-rules.md) for remaining gaps.

Treat repository authorities and `.codewright.toml` as read-only inputs unless the current task explicitly changes them or the user accepts the first-use setup below. A repository authority always overrides the profile. When repository authorities conflict, follow the nearest applicable authority and report the stale pair.

## First Use And Setup

For implementation, check the active repository root for `.codewright.toml` before exploring code. If it is absent, read [references/repository-language-profile.md](references/repository-language-profile.md) and offer its first-use setup once in the current conversation. Collect unresolved language choices and explain `ask` versus `auto` together. Continue grounding while the answer is pending; do not persist unanswered choices. If the user skips setup or gives no answer, continue the requested work with repository authorities and defaults. Review-only work stays read-only and does not prompt for setup.

When the user explicitly asks to configure Codewright, run the same setup whether or not a profile exists. Finish with the resolved settings, files changed, and any settings left at defaults. Do not search other projects for preferences or edit installed skill files to configure a consuming repository.

## Context Pointers

- **Baseline:** Always read [references/default-contribution-rules.md](references/default-contribution-rules.md) before implementation or review.
- **Code placement:** Read [references/code-placement-review.md](references/code-placement-review.md) when assigning new behavior to an owner, moving code or tests, or reviewing file placement, declaration order, or readability.
- **Repository profile:** Read [references/repository-language-profile.md](references/repository-language-profile.md) when `.codewright.toml` exists, first-use setup is offered, or the task creates or changes it. Missing approval settings default to `ask`.
- **CLI structure:** Read [references/cli-project-structure.md](references/cli-project-structure.md) when changing CLI topology, command dispatch, CLI test placement, or a CLI application's runtime mode, lifecycle, or platform boundaries.
- **Python code shape:** Read [references/python-code-shape.md](references/python-code-shape.md) when changing Python mappings passed between owners, validation code, or persistence interfaces.
- **TypeScript/React code shape:** Read [references/typescript-react-code-shape.md](references/typescript-react-code-shape.md) when changing client request helpers, API types, component props, or UI orchestration.
- **Rust:** Read [references/rust-contribution-rules.md](references/rust-contribution-rules.md) when the changed target is Rust.
- **Axum:** Read [references/axum-api-boundaries.md](references/axum-api-boundaries.md) when changing Axum handlers, extractors, middleware, request DTOs, or API schemas.
- **Svelte/SvelteKit:** Read [references/svelte-component-boundaries.md](references/svelte-component-boundaries.md) when changing Svelte components, reactivity, SvelteKit data loading, form actions, or rendering boundaries.
- **Prose editing:** When the authorized change includes a prose-editing pass for comments, API documentation, test descriptions, or maintainer documentation, resolve this `SKILL.md` through installation symlinks and read [shared prose editing](../references/prose-editing.md) relative to its real directory if that reference exists. If it is absent in a standalone installation, use the governing language settings, baseline prose rules, and normal verification and review criteria.

Read the baseline and only the references whose conditions match. Language and framework references can both apply. When no pointer matches, use the repository and baseline without substituting a nearby reference.

The English instructions and examples do not select the language of changed prose or the handoff. Apply the governing language choice separately to each code surface; follow the user's requested language for the handoff.

## Responsibility Boundaries

When an implementation changes an existing root, router, or shared orchestrator, compare the new behavior with that owner's current responsibility. A boundary concern exists when authority assigns the behavior elsewhere, independent concerns would share policy or lifecycle code, or a generic owner would depend on a concrete implementation. Repository authorities decide whether composition-root wiring belongs there.

Do not infer a boundary problem from size, imports, nesting, or pre-existing debt alone. Weigh consumer distribution, independent change axes, dependency direction, and required visibility alongside repository authority and the smallest callable surface; do not impose a fixed module taxonomy.

Treat a module split as a boundary change, not a file move. Identify the dependency direction and smallest callable surface between the new owners. New cross-module visibility is not a violation by count alone, but each exposed item must represent a deliberate boundary operation. If implementation details are widened mainly so sibling modules or tests can reach them, regroup the behavior, nest the consumers or tests under its owner, or expose a cohesive operation instead.

## Run

### Review-only

When the user requests inspection without edits, run **Ground** and **Review** against the requested state. For a working-tree review, include staged, unstaged, and untracked changes; for a branch review, use the requested base or range. Use read-only checks as needed and state which checks ran. Finish with findings or an explicit no-findings verdict, placement rationale, and verification limits. Leave files unchanged; **Confirm shape**, **Implement**, and implementation completion criteria apply only to authorized changes.

### Implementation

1. **Ground.** Read the governing sources, current tree, entry point, nearest owners, tests, and diff. For each requested behavior, name the smallest repository-authorized owner. When it touches a root, router, or shared orchestrator, state that owner's existing responsibility and apply the responsibility-boundary check above before editing. If the check finds an authority conflict or a concern that the approved scope and existing shape do not resolve, request an owner decision before editing. Finish with the requested behavior, intended owners, and verification surface stated explicitly; label assumptions.
2. **Confirm shape.** When the change introduces or moves a directory, module, or test hierarchy, show the proposed tree, one responsibility per part, and the intended dependency direction and shared surface between parts. An existing approved hierarchy satisfies this step when the change extends it consistently without widening that surface. Otherwise, `approval.shape = "ask"` (the default) waits for approval; `"auto"` continues after that brief explanation only when the shape stays within the requested task and ownership is settled. Auto approval does not settle new product, security, trust, or ownership decisions, override a user or repository requirement to wait, or grant tool permissions or external-action authority. Resolve those decisions before editing, regardless of this setting.
3. **Implement.** Change one cohesive scope. For a behavior-preserving refactor, name the concrete maintenance cost and preserved contract before editing; keep discovered behavior changes in a separately authorized scope. Update its owned tests and documentation when the change affects them. If implementation reveals a boundary concern or conflicts with governing ownership and the approved scope and shape do not resolve it, stop and request an owner decision. Finish when every changed line belongs to that scope.
4. **Verify.** Run the repository formatter, compiler or linter, and nearest meaningful tests. Finish with each required check passing or its missing result explained. A moved test is verified only by a command that discovers or compiles its new location.
5. **Review.** Read the final diff and tree against every governing source and repeat the boundary check. Assess file ownership and in-file declaration order separately; use the code-placement reference when its trigger applies. If a structural change affects two or more children of one parent, review their combined final topology; justify sibling-versus-child placement with the evidence above, including authorized entrypoint or public surfaces, and descend support code with one clear owner when the dependency direction permits. Separate scope reviews do not replace this parent-scoped pass, and shorter listings alone do not justify grouping. Resolve known stale paths, ownership, visibility, comments, test placement, or unrelated churn within the authorized scope, or report the finding. Compare claims in the changed scope with actual behavior, boundary conditions, and governing contracts. A review covers only the state it inspected; after review-driven edits, run affected checks and re-review the updated final diff in any user-requested review mode before completion.

## Done When

For setup-only work, the requested settings are saved and validated, unrelated content is preserved, and the handoff names the effective settings and files changed. A skipped optional setup creates no files. Implementation completion requires:

- the requested code, test, or placement change is complete and affected tests are updated;
- every changed responsibility has a clear owner, and every changed file follows the applicable rules;
- every required check passed, or each missing check has an explicit reason;
- the handoff names the outcome, verification, and unresolved decisions;
- commit readiness is claimed only when no owner decision remains unresolved and no known rule violation remains.
