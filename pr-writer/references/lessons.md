# Maintenance evidence

This record explains reusable changes to the skill. It is not a required input
for normal PR writing and does not store production incident data.

## 2026-10-12 — Draft and edit comparison

An authoring session compared an initial PR body with its edited version. The
edited body put repeated input-policy conditions in a table and grouped checks
by their evidence scope. The reader found it clearer. The installed skill
already required both drafting and whole-document editing, so this comparison
supports applying those instructions earlier; it does not prove that a new
skill outperforms the old one.

- Make representation choice part of drafting, with an optional worked example.
- Reconcile policy semantics and evidence scope after editing. Required values,
  defaults, sentinel normalization, existing values, and execution exclusions
  are easy to accidentally broaden while shortening text.
- Pin the prose editor through a Git submodule; keep the editing pass executable
  when its checkout is uninitialized.
- Keep repository rules and incident facts in their actual sources. Examples use
  fictional values and counts, not customer identifiers or operational logs.

Calibration sources:

- [AI Hero: writing-for-agents](https://www.aihero.dev/skills-writing-for-agents)
- [AI Hero: pr](https://www.aihero.dev/skills-pr)

Structural validation does not establish writing quality. Fresh-context review
and an execution exercise should report their actual evidence and limits.

## 2026-10-12 — Fresh-context checks

Two agents started without the authoring conversation. One applied the repository's
skill-reviewer criteria and current AI Hero exemplars to the package and returned
Ready with no Major or Minor findings. It checked the type routes, publication
branch, embedded editor binding, metadata, and pinned gitlink.

The other used the skill to draft a Korean bugfix PR from a real commit, its
parent, the repository template, code, and existing test artifacts. Its output
kept conditional input behavior in a table, distinguished 35 added regression
cases from the suite's 2,182 passes and 4 skips, separated inspection from test
evidence, and disclosed the excluded live test. It reported no skill defect.

This is one execution case, not a comparative benchmark or evidence that every
change type and remote publishing path has been exercised. The existing test
artifacts lacked a source SHA; the agent reported them as supplied prior results,
not a new execution or an independently certified check of the commit bytes.
