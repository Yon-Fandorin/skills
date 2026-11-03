---
name: finish-task
description: Wrap up completed work by cleaning up its local byproducts and reconciling final records. Use when the user asks to finish a task, remove its leftovers, or consolidate plans and interim notes. Preserve deliverables, useful evidence, and unrelated work.
---

# Finish a task

Preserve the completed result and reusable evidence while removing this task's
byproducts and reconciling its records. Apply when the user requests task
wrap-up or cleanup.

## Establish scope and completion

- Read the current task, existing authorizations, access restrictions, and
  applicable `AGENTS.md` files. If the user closed production access, keep it
  closed. Describe an offline check as an offline check.
- Distinguish implementation, tests, PR creation, merge, deployment, and
  production verification. Complete remaining work required by the original
  request before treating cleanup as the end of the task.
- Finish related remote changes when existing authorization covers them. For
  changes outside that scope, prepare a concrete, reviewable result before
  asking. Cleanup does not itself authorize a new deployment, PR merge, or
  production mutation.

## Identify this task's byproducts

Use the conversation and file, Git, or resource metadata to establish ownership.
A matching name or creation time alone is insufficient. Select exact targets;
leave shared directories intact.

Inspect the categories used by this task:

- Temporary scripts, research downloads, validation configurations, repeated
  outputs, intermediate JSON, and PR body drafts.
- Task checkouts, local branches, downloaded dependencies, and build outputs.
- Test containers, networks, volumes, images, port forwards, and background
  processes.
- Plans, progress reports, final records, indexes, and incoming references.

Keep deliverables, evidence needed to support conclusions, and reproductions
for unresolved issues. Preserve credentials, environment files, and user
settings even when Git ignores them. Before deleting raw evidence, retain the
necessary conclusion, provenance, and verification limits in the final record.

## Clean Git and shared resources

- Check tracked, untracked, and ignored files before removing a task checkout.
  Ignored files can contain secrets or user work. Remove only identified task
  byproducts such as downloaded validation dependencies.
- Confirm that branch contents are preserved before deleting the checkout or
  branch. For a squash merge, compare the merged PR and commit with the final
  contents of all task changes; ancestry alone is insufficient. Keep additional
  commits or unrelated changes that have not been preserved.
- Remove the task checkout before its local branch. Preserve other checkouts,
  branches, and uncommitted work. Do not force-reset or overwrite work to make
  deletion possible. Remote branch deletion is a separate scope decision.
- For Docker images, check exact references and users among running and stopped
  containers. Delete volumes only when task ownership and non-use are proven.
  Preserve unidentified anonymous volumes and avoid global prune commands.
- Identify processes by command, target, and task context before stopping them.
  A matching process name alone is insufficient.
- Treat snapshots, production backups, and cloud volumes separately from local
  byproducts. Require existing deletion authorization and the necessary
  verification. Record a deleted recovery point as unavailable.

## Reconcile final records

- Search related plans, indexes, and linked source runbooks as well as the last
  note. Resolve stale statements such as "not applied", "in progress", or
  "backup retained" that contradict the final state.
- Update the existing topic document. Retain the cause, final action, observation
  date and scope, meaningful validation evidence, and remaining limits. Keep
  detailed procedures with their owning repository and link to them.
- Transfer reusable procedures and future checks before removing redundant
  drafts, progress reports, or repeated output. A policy change does not prove
  that its full retention period has elapsed successfully.
- Update incoming links and indexes when deleting or moving files. Preserve
  unrelated incident records and other contributors' edits.
- When the remote source cannot be updated, identify its exact path, the stale
  claim, and the remaining action. A corrected local summary does not establish
  that every source record has been reconciled.
- Avoid a separate report, file inventory, or movement history about the cleanup
  itself unless the user or applicable repository instructions require one.
  Keep secrets out of records.

## Verify the final state

Check the absence of the exact paths, branches, and resources removed, the state
of work being preserved, and the facts, dates, and links in changed records.
Remove temporary files created during cleanup too. Repeat tests or reconnect to
production only when necessary and authorized for this verification.

Report the cleanup categories, final record links, and any remaining work or
verification limits briefly. Distinguish observed results from inferences and
prepared changes. Claim completion only for deletions, edits, and remote updates
that actually finished.
