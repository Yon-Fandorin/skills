# Fresh-context completion review

This is the common completion gate for deliverables, independent of project
type. A delegated review worker reports its findings to the caller instead of
recursively dispatching another review of its own report.

1. Give a new reviewer the final artifact snapshot, raw task requirements,
   approved constraints, applicable authorities, and actual verification
   evidence. Disable conversation inheritance (`fork_turns: "none"` in Codex).
   Keep authoring history, desired verdicts, and earlier review conclusions out
   of the brief. Choose review criteria appropriate to the artifact; Skill
   Reviewer is for skill packages, not arbitrary application code.
2. Have the reviewer inspect the artifact read-only and report evidence-backed
   defects or improvements to the requested result, with scope and limitations.
   A preference alone or unrelated scope expansion is not an actionable finding.
   Reconcile findings against the actual artifact; never require a favorable
   verdict or discard a supported finding just because it is minor.
3. Resolve actionable findings within the authorized scope. After corrections,
   run affected verification and send the final snapshot to another fresh-context
   reviewer. Continue until that snapshot has no unresolved actionable findings.
   The author checks that the report covers the actual final state; a report
   from before the latest edits cannot close the gate.
4. If findings require a new user decision or external authority, or the required
   reviewer or checks are unavailable, report what remains incomplete and seek
   only the missing decision. Do not replace the required independent review
   with a self-review or claim completion with unresolved findings.

The completion record identifies the final snapshot, reviewer independence,
scope, actual checks, and final findings. Follow project rules for where review
records belong. Report the limits of the evidence; a clean scoped review is
not a guarantee against every future defect.
