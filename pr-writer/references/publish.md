# Publish or update a PR

Use this reference when the user has requested PR creation or modification. The writing task alone does not authorize publishing, merging, or deploying.

## Before writing to the hosting service

- Verify the user's intended base branch and source branch. Inspect the comparison and included commits/files so unrelated working changes do not enter the PR. Preserve unrelated work; isolate this change when needed.
- For an existing PR, inspect its current base, head, title, body, labels, and relevant repository conventions before making the requested update. A body-only update should retain unrelated metadata.
- For related PRs, verify companion links and contract-dependent rollout order. Distinguish required dependencies from optional coordination; describe undeployed behavior as such.
- Select the repository's existing type label from the chosen PR type. Use an exact match or verified equivalent, retain unrelated labels, and leave labels unchanged if no equivalent exists. Report that mismatch instead of creating a label. The type label does not need a body section.

## Apply and verify

Use structured title/body arguments where available. With a CLI, put the exact Markdown in a file and pass its body-file option to preserve newlines and literal text.

Read back the PR title, body, base, head, and labels after the operation. Compare with the intended artifact and metadata; verify the included change scope when creating a PR or changing branches. Correct mismatches within the authorized request and report any remaining limitation. Completion requires the published result, not merely a successful write command.
