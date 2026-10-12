# Codewright Lessons

## Behavior-Preserving Structure Review

A request to improve code quality can concern maintenance cost rather than runtime defects. The recipe now asks a refactor to name that cost and its preserved contract. Newly discovered bug fixes remain a separate scope so successful tests cannot conceal a changed refactoring objective.

Keep the core language- and framework-independent. Conditional references supply ecosystem-specific alternatives only when the task reaches them. Derive model choice, placement, and verification commands from the consuming repository; a successful project-specific refactor is not a universal template.

AI Hero's [writing-for-agents](https://www.aihero.dev/skills-writing-for-agents) is the authoring standard: explicit branch pointers, checkable completion, and the behavioral no-op test. [Codebase-design](https://www.aihero.dev/skills-codebase-design) supplies the deletion test; [code-review](https://www.aihero.dev/skills-code-review) keeps repository standards distinct from heuristics.

Validate additions on identical raw artifacts and requests with fresh execution. Equivalent outcomes invite the behavioral no-op test; prune instructions with no demonstrated decision value instead of counting them as improvements. A small smoke sample records observed choices and parity; it does not establish general superiority.

Keep project cases, patches, and smoke outcomes in the evaluation report. Promote only the supported decision criterion into this skill: compare removed caller obligations with added interface and coupling costs, preserve independently changing policies, and allow the existing structure to remain when a change has no demonstrated benefit.

## Language And Framework References

The former `rust-style`, `rust-axum-backend`, and `svelte5` packages at
`Yon-Fandorin/skills` revision `61455600d95ed5227a69f708348a7f50a86fd1cf`
mixed implementation recipes with ecosystem rules. Keep one implementation and
review workflow; route language and framework decisions separately.

Preserve private test ownership, extractor/body order, nullable-update states,
and server/client boundaries. Derive versions and project policies from the
target repository. Public API renames, custom error macros, a fixed HTTP error
status, module taxonomy, and wholesale Svelte syntax migration require local
authority or task scope; they are not framework defaults.

The new references summarize decision boundaries and point to primary docs for
version-sensitive mechanics. They do not retain the old copied API manuals or
force every framework reference into unrelated work.
