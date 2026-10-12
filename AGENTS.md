# Repository instructions

This repository owns `codewright`, `pr-writer`, and `skill-reviewer`. Shared prose
editing is defined in `references/prose-editing.md`; Humanizer's upstream source
is the pinned `external/humanizer` submodule. Follow the authoring-language
convention in the root README, including examples in the artifact's language.

## Document review inventory

For documentation or skill-instruction work, maintain `docs/document-review.md`
as the complete file inventory and review record. Enumerate tracked parent files
and the tracked files of each relevant submodule, including hidden metadata,
instead of relying on a remembered file count or a Hangul-only search.

Mark new, changed, or moved files unchecked before review. Check a file only after
reading its final content, resolving material findings, and completing the
applicable link, metadata, or workflow checks. Reopen it after further edits.
Record the review scope, source revision, reviewer, and what the checks establish.

When independent agents are requested, give each an explicit file set and keep
their edits disjoint. Reconcile their reports with the final files before the
integration verdict. A completed subtask or a matching hash alone does not
establish that its content and runtime claims are correct.

Keep external source files unchanged during local documentation work. Record
upstream checks separately from this repository's integration checks, and state
unexecuted checks without marking them as passing.
