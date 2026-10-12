# Editing examples

Use these examples for conditional behavior or a dense PR body. The policies
and counts below are fictional; derive the actual PR's facts from its artifacts.
They illustrate representation choices, not required fields or headings.

## Conditional behavior

A policy paragraph makes the reader reconstruct the comparison:

> Strict schedules require `startDay` from 1 to 28. Flexible schedules accept
> omission or null and convert 0 to null while retaining other values. In strict
> schedules `chargeDay` must be 1 to 31; omitting it uses the existing default 1.

The same policy is easier to compare in a table:

| Schedule | `startDay` | `chargeDay` |
| --- | --- | --- |
| Strict | Required, 1–28; omission, null, 0, or other out-of-range values return 400 | 1–31; omission defaults to 1 |
| Flexible | Omission/null stay null; only 0 becomes null; other values stay unchanged | Existing behavior |

An edit that says “both dates are required” changes the default rule. An edit
that says “flexible dates are cleared” changes the preservation rule. Either
fails reconciliation even if it reads smoothly.

## Execution boundary

“Validate before saving” leaves the ordering of other effects unclear.
If inspection establishes it, use the meaningful boundary instead:

```text
request → validate → mutate price → publish event → save
```

Include only boundaries supported by the actual path. A response-and-DB test
does not by itself prove event ordering; label inspection evidence accordingly.

## Validation scope

Suppose an execution artifact records 9 added regression cases and 2 existing
focused cases passing. A suite artifact records 100 passes and 3 skips, while an
external-service test was excluded from execution.

A compact report preserves those distinctions:

- Focused checks: 9 added regression cases plus 2 existing cases passed;
  responses and persisted state were checked.
- Suite: 100 passed and 3 skipped under the recorded environment;
  the external-service test was excluded from execution.

“11 new tests passed” overstates the additions. “All tests passed” hides the
skips and exclusion. Include execution conditions when they affect confidence
or reproduction; keep incidental investigation logs in the private ledger.

## Dense existing body

When revising an existing description:

1. Keep the concrete problem and resulting behavior in the opening.
2. Consolidate repeated conditions or mappings into one comparison.
3. Keep supporting fixture/configuration rationale where its purpose is unclear.
4. Place limits beside the checks they qualify, then compare claims with sources.

A small change that is already clear can keep its short prose form. The purpose
of editing is easier comprehension with the same supported meaning.
