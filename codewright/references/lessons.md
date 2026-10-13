# Codewright Lessons

Keep reusable decision criteria here. Store project cases, patches, comparison
outputs, and execution history in private review records.

## Behavior-preserving changes

Name the concrete maintenance cost and the contract a refactor must preserve.
Keep newly discovered bug fixes in a separate scope so passing tests do not
conceal a change to the refactoring objective.

Compare the caller obligations an abstraction removes with the interface and
coupling it adds. Preserve independently changing policies and retain an existing
structure when no observed cost justifies changing it.

## Language and framework boundaries

Keep the implementation and review workflow independent of language and framework.
Load ecosystem references only when the task reaches their decisions. Derive types,
placement, dependency versions, and verification commands from the consuming
repository.

Preserve private test ownership, extractor/body order, nullable-update states,
and server/client boundaries. API renames, custom error macros, fixed HTTP error
statuses, module taxonomies, and syntax migrations need repository authority or
task scope. They are not framework defaults.

Keep version-sensitive mechanics in primary documentation. References should
explain decision boundaries without duplicating API manuals.

## Evaluating instructions

Compare instructions using the same raw artifacts and requests with fresh
execution. Prune additions that have no demonstrated decision value. Record
observed choices, evidence scope, and limitations; a small smoke sample or
equivalent output does not establish general superiority.

## Authoring sources

- [Writing for agents](https://www.aihero.dev/skills-writing-for-agents): branch pointers and observable completion.
- [Codebase design](https://www.aihero.dev/skills-codebase-design): caller cost and the deletion test.
- [Code review](https://www.aihero.dev/skills-code-review): repository standards versus heuristics.
