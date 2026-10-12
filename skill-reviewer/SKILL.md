---
name: skill-reviewer
description: >-
  Review new or edited Agent Skills in a fresh-context agent, using AI Hero
  writing guidance and a matching exemplar to check triggers, structure,
  executable steps, completion criteria, and package consistency. Use when
  assessing whether a skill is ready. Read-only by default. Not for behavioral
  evals, adversarial hardening, or application code review.
---

# Skill Reviewer

Review one skill package against its intended contract and evidence. Keep a small set of material findings.

## Context pointers

- **Criteria:** Read [review criteria](references/review-criteria.md) for every review.
- **Calibration:** Read [exemplar selection](references/exemplars.md), then the AI Hero writing source and the matching skill source it selects. A summary or unopened link does not complete calibration.
- **Report editing:** When the report needs a prose pass, resolve this file through installation symlinks and read [shared prose editing](../references/prose-editing.md) relative to its real directory if present. In a standalone installation, use the finding filter and output rules below.

## Dispatch

If assigned as the review worker, perform **Review** directly and return the report. Keep delegation with the caller; do not invoke this skill again or spawn another reviewer.

Otherwise, dispatch one new agent with conversation inheritance disabled. In Codex's collaboration API, use `fork_turns: "none"`; in other hosts, use the equivalent fresh-context option. Give it:

- This skill's path and the explicit role **review worker**.
- The target package path, governing instruction paths, review scope, and the user's requirements as raw task evidence.
- The exact file snapshot or revision to inspect, including uncommitted files when they are the target.
- Read-only permissions, report destination and language, and any supplied reference snapshot with its source URL and revision.

Keep authoring history, proposed verdicts, suspected defects, and earlier review conclusions out of the brief. The worker reads the files itself and returns its own evidence. A summary of the authoring conversation is not a fresh review.

If fresh delegation is unavailable or prohibited, perform a local review, record that independence was not checked, and use `Review incomplete` for the final status.

## Review

1. **Contract.** Read the target `SKILL.md`, governing instructions, and any UI metadata or catalog entry. State the trigger, inputs, output, invocation mode, and boundary in your own words.
2. **Map.** Inventory package files and pointers. Read every reference reached by the default path and the branch under review. Check target existence, loading conditions, and whether required material can be reached.
3. **Calibrate.** Read the writing guidance and one matching exemplar selected by the calibration reference. Compare information hierarchy, co-location, workflow, and stopping conditions with concrete target locations. Record the sources actually read, their revision or retrieval date, and the patterns used.
4. **Review.** Apply every criteria axis. Trace a representative request from trigger to output through the selected branch. Record checked axes and any unexamined branch; this walkthrough does not establish behavioral test results.
5. **Filter.** Keep a finding only when it cites an exact location, provides evidence, predicts behavior or maintenance impact, and names the smallest correction. Remove preference-only comments.
6. **Report.** Return findings, coverage, and a verdict under the output rules. Review only; change the package only when the user has requested revisions.

## Reconcile

The caller checks each retained finding against the inspected files and verifies the report's coverage and sources. A missing report, skipped axis, or changed snapshot leaves the affected review incomplete. After an authorized fix, recheck the affected files and paths; keep untouched evidence and stop when the requested scope is complete.

## Output

Use the user's or repository's language for prose and headings. Keep the literal severity labels `Major` and `Minor` and status values below. Editing a report preserves each finding's location, evidence, impact, correction, and severity.

```markdown
## Findings

- Major — `path:line` — evidence — impact — smallest correction
- Minor — `path:line` — evidence — impact — smallest correction

## Coverage

- Scope and inspected snapshot:
- Mode: fresh-context worker | local review
- Sources read and comparison patterns:
- Axes and branches checked; remaining checks:

## Verdict

Ready | Revisions required | Review incomplete
```

`Ready` requires a fresh worker, completed calibration, and all criteria axes checked for the declared scope, with no Major finding. A Major finding yields `Revisions required`. Minor findings may accompany `Ready`. Use `Review incomplete` when required checks could not finish; identify the missing check without treating tool or source unavailability as a package defect. If no findings survive the filter, write `No findings` and retain the coverage record.
