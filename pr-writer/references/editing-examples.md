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

## Validation summary

Suppose logs contain individual test names, reruns, suite totals, and temporary
paths. The relevant result is that a regression check now preserves an explicit
zero value and the focused checks pass. Live external-service behavior was not
tested and matters to the review.

A suitable summary is:

> The zero-value regression check and related local checks pass. Live
> external-service integration remains unverified.

The reviewer learns what is supported and what remains uncertain without the
execution transcript. Omit counts and test-file inventories unless they change
the review decision. If a repository template requires commands, keep the
relevant command and result in its required field. A regression check not run
must remain unverified, even when shortening the text. Do not summarize a
partially checked change as "all tests passed."

## Review revisions

Suppose the comparison base uses a truthiness fallback that replaces explicit
zero with a default. An intermediate draft rejected zero, but review fixes
removed that validation; the final patch defaults only an unspecified value.

An appended update leaves conflicting descriptions:

> Zero is rejected. After review, we changed validation to accept zero instead.

Rewrite from the final comparison:

> Explicit zero now remains zero instead of becoming the default. Only an
> unspecified value uses the default.

The intermediate rejection is not part of the final change. If it had shipped
and required a migration or affected users, retain that operational consequence
instead of deleting relevant history. Any test result for the rejected-value
draft must be revalidated or left unverified for the final patch.

## Dense existing body

When revising an existing description:

1. Keep the concrete problem and resulting behavior in the opening.
2. Consolidate repeated conditions or mappings into one comparison.
3. Keep supporting fixture/configuration rationale where its purpose is unclear.
4. Place limits beside the checks they qualify, then compare claims with the
   final diff and applicable sources, including changes made during review.

A small change that is already clear can keep its short prose form. The purpose
of editing is easier comprehension with the same supported meaning.
