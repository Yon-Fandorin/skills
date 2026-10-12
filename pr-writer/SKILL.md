---
name: pr-writer
description: >-
  Draft or revise pull request titles and descriptions from the actual changes
  and validation evidence. Preserve repository templates and clarify behavior,
  cause, and merge implications. Create or update the PR only when requested.
---

# PR Writer

Deliver a PR a reviewer can understand without the conversation. Keep the
requested scope: draft, revise, or publish. This workflow describes the change;
it does not establish an independent code review.

## 1. Establish the facts

Inspect the request, repository instructions, relevant diff and commits, PR
template, and available validation artifacts. When revising an existing PR,
verify its inherited claims against the current change.

Resolve the comparison base from the user first, then verified task or repository
context. For a draft, identify the relevant diff; for publishing, also verify the
intended base branch and included changes. A default branch alone does not
establish the intended base. Surface ambiguity when it changes the PR's scope.

For consequential claims, keep a private ledger:
`claim | source | status | revision/environment scope`. Distinguish observations,
user-provided facts, and planned work. Reuse earlier checks only while their
relevant behavior remains unchanged; otherwise obtain new evidence or state the
remaining verification need. Keep investigation records out of the PR body.

**Complete when:** the changed behavior and cause are supported, the comparison
scope is known, consequential claims have traceable evidence, and required
template fields and language are recorded. Mark unavailable required values
unresolved instead of guessing.

## 2. Draft for the reviewer

Read only the closest type's reviewer questions:
[bugfix](templates/bugfix.md), [feature](templates/feature.md),
[refactor](templates/refactor.md), [performance](templates/performance.md),
[infra](templates/infra.md), or [hotfix](templates/hotfix.md).
Use [default](templates/default.md) when no type fits. Map the material questions
into the repository template once; its headings and metadata take precedence.
With no repository template, use only the headings this change needs.

Resolve the title and body language from the current user instruction, then
repository requirements, then the existing PR or supplied writing sample. When
none selects a language, use the user's language. The English instructions and
type-template headings are guidance; adapt optional headings to the resolved
language while retaining headings and metadata required by the repository.

Lead with the concrete problem and resulting behavior. Give each fact one home:

- **Change:** observable behavior and affected paths.
- **Reason:** causal explanation, the chosen correction, and relevant constraints.
- **Implementation:** mechanisms and execution boundaries needed to assess the fix.
- **Evidence:** what each check establishes, its result, and material limits.
- **Merge implications:** compatibility, dependencies, recovery, and review focus.

These are information roles, not additional required headings. Keep supporting
configuration or fixture changes when their purpose would otherwise be unclear.

Choose the representation while drafting: prose for one causal chain, bullets
for parallel facts, tables for repeated condition-to-outcome comparisons, and a
short flow for essential order. Small changes can remain a few sentences.
For input-policy changes, account for applicable omission, null, sentinel,
default, and valid-value behavior in the comparison. Name the protected action
when order matters, such as validation before mutation or event publication.
For worked examples, read [editing examples](references/editing-examples.md)
when drafting conditional behavior or restructuring a dense body.

Group validation by what it proves. Distinguish added regression cases from
existing cases or suite totals when reporting counts, and skipped cases from
tests excluded from execution. Keep the checked environment and consequential
limits beside the result. A planned check remains a plan, not a passing result.

Describe meaningful persistent-state effects, including a supported recovery
path or the known unresolved constraint. Infra and hotfix changes need a concrete
rollback plan. For companion PRs, identify the contract dependency and verified
link; put required deployment order where it first affects using the change.
Keep each PR's evidence scope separate.

Write a concise outcome-oriented title using the repository's convention.

**Complete when:** the problem, behavior, cause, evidence, and merge implications
are easy to find; required template items and material type questions each have
one home; comparisons and critical order are visible in the chosen structure.

## 3. Edit and reconcile

Edit the whole body before returning it. Resolve this `SKILL.md` through
installation symlinks and read [shared prose editing](../references/prose-editing.md)
relative to its real directory when that reference exists. It owns shared
Humanizer resolution and language-aware editing. If the reference is absent in
a standalone installation, perform the pass below directly; the same completion
criteria apply.

Rebuild the reading order rather than appending new facts. Remove repeated
explanations, file inventories, and investigation chronology. Retain details
that change the reviewer's understanding, confidence, or review action. Preserve
the resolved language, required headings, identifiers, commands, and links.

Compare the edited body with the ledger: conditional requirements and defaults,
normalization scope, execution order, evidence counts and exclusions, and merge
conditions must retain their meaning. Separate code inspection, test execution,
browser checks, and production verification where the distinction matters.

**Complete when:** the opening states the problem and outcome, each section
answers a distinct reviewer question, conditions are easy to compare, and every
consequential statement retains its supported scope. The normal deliverable is
the edited artifact; show intermediate versions when the user requests them.

## 4. Return or publish

For a draft, return the title and body with material unresolved inputs.
When PR creation or modification is authorized, read
[publishing](references/publish.md) for branch, scope, label, and readback checks.

**Complete when:** the requested artifact is delivered; for publishing, the
hosting service's title, body, base, head, and labels have been read back and
match the intended result. Stop at the requested outcome.
