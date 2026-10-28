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
verify its inherited claims against the current change. Use the final
base-to-head comparison, not just the latest commit or an earlier draft.
Review-driven fixes can invalidate both the description and prior evidence.

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
- **Evidence:** concise support for the behavior claim and material limits.
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

Summarize relevant validation by the behavior checked and its outcome, usually
in a short sentence. Keep failures and missing verification that affect review
or merge confidence. Omit incidental commands, test names or paths, raw counts,
rerun history, and environment details unless needed to assess or reproduce
the result, or required by the user or repository template. An irrelevant check
does not need a section merely to say it was not run.

When counts or execution details are useful, keep their scope accurate: added
cases are not suite totals, and skipped or excluded tests did not pass. Avoid
blanket success claims that hide relevant limits. Keep full logs and evidence
provenance outside the body. For noisy results or missing checks, read the
[validation examples](references/editing-examples.md#validation-summary).

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

Select reviewer-relevant facts before the prose pass. Resolve this `SKILL.md` through
installation symlinks and read [shared prose editing](../references/prose-editing.md)
relative to its real directory when that reference exists. It owns shared
Humanizer resolution and language-aware editing. Apply the resolved Humanizer
instructions to the selected title and body in embedded mode, returning only
the final artifact. If the shared editor is unavailable in a standalone
installation, perform the native pass below without fetching a dependency.

Read the title and body as a reviewer encountering the change for the first
time. Make the problem, resulting behavior, and review implications easy to
follow. Keep paragraphs focused; use lists or tables where comparison benefits.
Remove repeated explanations, file inventories, investigation chronology,
decorative formatting, and empty sections. Preserve the resolved language,
required headings, and the identifiers, commands, and links still needed.

### Final-state self-review

After editing, recheck the title and body against the latest base-to-head diff,
final implementation, and applicable evidence, including fixes made during
review. Confirm the current scope, behavior, paths, and verification claims.
An old description or passing result does not establish the revised state.

Rewrite around the original problem, its cause, and the final solution. Remove
superseded approaches, reverted changes, review conversations, and chronological
patch notes. Keep before/after behavior and any shipped-state, migration,
compatibility, or recovery history that still affects review or operation.
For an earlier draft that survived review fixes, read
[review revisions](references/editing-examples.md#review-revisions).

Reconcile retained claims with the ledger, preserving conditions, defaults,
order, material verification limits, and merge implications. If review fixes
invalidate a check, obtain relevant evidence within the authorized scope or
report the current gap. Keep inspection, tests, and live checks distinct where
confidence depends on them; do not restore discarded operational detail.

If this pass changes substantive prose, apply the prose editor again and
recheck the affected claims. Repeat the affected pass if the comparison changes
before delivery. Keep this audit internal unless requested.

**Complete when:** the opening states the problem and outcome, each section
answers a distinct reviewer question, conditions are easy to compare, and every
retained consequential statement matches the final comparison. The reader can
understand the change without reconstructing the work or review log. Return
the edited artifact; show
intermediate versions or an editing audit only when requested.

## 4. Return or publish

For a draft, return the title and body with material unresolved inputs.
When PR creation or modification is authorized, read
[publishing](references/publish.md) for branch, scope, label, and readback checks.

**Complete when:** the requested artifact is delivered; for publishing, the
hosting service's title, body, base, head, labels, and draft state have been read
back and match the intended result. Stop at the requested outcome.
