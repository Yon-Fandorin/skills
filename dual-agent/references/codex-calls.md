# Codex calls (Claude Code host)

Under a Claude Code host, the Codex roles run through `codex exec`. The common rules under "Counterpart calls" in SKILL.md apply to every call.

## Flags

Every call uses `"$TIMEOUT" <seconds>`, `-c approval_policy="never"`, `-C "$ROOT"`, `-o <output file>`, `</dev/null`, and redirects its log to a file. The sandbox depends on the role:

| Role of Codex | Sandbox | Output | Prompt must say |
|---|---|---|---|
| Critic (Phase 1-2, and Phase 4 discussion) | `-s read-only` | `-o` `critique-*.md` | the lenses to apply; modify no file |
| Author (`lead = codex`: drafts or revises `problem.md` or `design.md`) | `-s workspace-write` | `-o` the final message; the artifact itself is written at its path | write only that artifact path; change no other file; when revising, read the critique file and mark each point accept, rebut (with evidence), or defer |
| Reviewer (`reviewer = codex`, Phase 4) | `-s read-only` | `-o` `review-rN.md` | review `diff-rN.patch` and `checks-rN.txt` against `design.md` with the Phase 4 lenses; tag severity and disposition; modify no file |
| Worker (Phase 3 and `FIX` redelegation) | `-s workspace-write` | `-o` `impl-rN.last.md` | implement `design.md` (or the listed `FIX` items) only; do not commit; list questions |

Build the author and reviewer calls from the critic and worker commands below.

## Critic

```bash
"$TIMEOUT" 1500 codex exec -c approval_policy="never" -s read-only -C "$ROOT" \
  -o "$RUN/critique-problem-r1.md" \
  "Read problem.md and verify against the codebase directly, then critique it. Keep exploration focused and finish within about 15 minutes. <lenses from the phase>. Cite file:line evidence for each point and confirm agreements briefly. Do not modify any file. User direction: <verbatim>. File: $RUN/problem.md" \
  </dev/null > "$RUN/problem-r1.log" 2>&1
```

## Worker

```bash
"$TIMEOUT" <worker_timeout_sec> codex exec -c approval_policy="never" -s workspace-write -C "$ROOT" \
  -o "$RUN/impl-r1.last.md" \
  "Implement design.md. Make no change outside its scope. Do not commit; leave changes in the working tree. Run the tests if any exist and report the result. For anything that conflicts with the design or is unclear, do not decide on your own; list it under 'Questions:' in your final message. User direction: <verbatim>. File: $RUN/design.md" \
  </dev/null > "$RUN/impl-r1.log" 2>&1
```

## Codex-specific rules

- A run is successful only when the exit code is 0 **and** the `-o` file exists and is non-empty. A run killed by the time limit writes no `-o` file.
- Keep `approval_policy="never"`: a user configuration that reviews or auto-approves escalation requests can otherwise let a `read-only` run write files. Do not use `--dangerously-bypass-approvals-and-sandbox`. When a task needs network access (for example `npm install`), tell the user and open only that setting.
