# PR Writer Lessons

Keep reusable writing and verification principles here. Store specific PRs,
evaluation runs, test counts, and authoring history in private review records.

## Choose the representation while drafting

Use a table when repeated input-policy conditions are easier to compare there.
Group checks by what their evidence establishes. A short, clear change can remain
prose; a template does not require every heading for every PR.

## Preserve meaning during editing

Reconcile required values, defaults, sentinel normalization, unchanged values,
and execution exclusions after shortening the text. Keep repository policy and
incident facts in their actual sources. Worked examples use fictional values
and counts rather than customer identifiers or operational logs.

The final base-to-head comparison owns the PR's scope. Review fixes may retire
earlier explanations and checks. Retain relevant before/after and shipped-state
consequences while removing the author's intermediate implementation history.

## Keep evidence traceable

Select evidence for the review decision before editing prose. Summarize the
relevant behavior and outcome; keep detailed commands, counts, and execution
history in private records unless they affect confidence or reproduction.
If counts are included, distinguish added cases from suite totals and skipped
cases from tests excluded from execution. Keep material limits visible.

Record source revision and environment privately when available. A supplied
result without a known revision does not certify the current commit. Disclose
that limit when it affects a retained claim; an accurate concise summary need
not reproduce the provenance ledger.

## Keep editing portable

Pin a shared editor through the repository's Git submodule and retain the
native editing pass when its checkout is unavailable. The editor must preserve
the caller's output language, scope, facts, and publication authority.

Structural validation does not establish writing quality. Fresh-context review
and execution exercises should report their actual coverage and limits. One case
does not establish comparative performance or exercise every change type and
publishing path.

## Authoring sources

- [Writing for agents](https://www.aihero.dev/skills-writing-for-agents)
- [PR writing](https://www.aihero.dev/skills-pr)
