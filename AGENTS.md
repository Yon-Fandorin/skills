# Repository instructions

This repository owns `codebase-architecture`, `code-wright`, `pr-writer`, and
`skill-reviewer`. Shared prose editing is defined in
`references/prose-editing.md`; Humanizer's upstream source
is the pinned `external/humanizer` submodule. Follow the authoring-language
convention in the root README, including examples in the artifact's language.

## Document review inventory

For documentation or skill-instruction work, maintain `docs/document-review.md`
as the current file inventory and durable review procedure. Enumerate tracked
parent files and the tracked files of each relevant submodule, including hidden
metadata, instead of relying on a remembered file count or a Hangul-only search.

Read each new, changed, or moved file's final content, resolve material findings,
and complete applicable link, metadata, or workflow checks. Recheck affected
content after further edits. Record the inspected snapshot, reviewer, actual
results, and unexecuted checks in private records outside version control.
Keep reusable criteria in lessons files; keep project examples, dated evaluation
results, commit-specific narratives, and task history out of public guidance.

When independent agents are requested, give each an explicit file set and keep
their edits disjoint. Reconcile their reports with the final files before the
integration verdict. A completed subtask or a matching hash alone does not
establish that its content and runtime claims are correct.

Keep external source files unchanged during local documentation work. Record
upstream checks separately from this repository's integration checks, and state
unexecuted checks without marking them as passing.
