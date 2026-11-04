# Claude calls (Codex host)

Under a Codex host, the Claude roles run through `claude -p` (Claude Code's non-interactive print mode). The common rules under "Counterpart calls" in SKILL.md apply to every call.

## Running outside the sandbox

`claude` needs network access and the user's Claude login, which the Codex sandbox usually blocks. Request the host's approval to run each `claude` call outside the sandbox, for that command only, with the justification described under "Counterpart calls" in SKILL.md. An approval review can reject a call that sends repository files to Claude when the request does not name the destination and purpose. Do not use `--dangerously-bypass-approvals-and-sandbox` and do not switch the whole session to full access. If the approval is refused or the call fails on authentication, stop and report.

## Flags

`claude` has no `-C`, so start every call with `cd "$ROOT" &&`. Put the prompt directly after `-p`: `--tools` and `--allowedTools` take a list, and a prompt placed after them is read as part of that list. Every call uses:

- `"$TIMEOUT" <seconds>` and `</dev/null`;
- `--no-session-persistence`, so the call leaves no session record;
- `--permission-mode dontAsk`, so a tool that is not explicitly allowed is denied instead of waiting for an answer;
- `--output-format text`, with stdout redirected to the output file and stderr to the log.

| Role of Claude | Tools | Output (stdout) | Prompt must say |
|---|---|---|---|
| Critic (Phase 1-2, and Phase 4 discussion) | `--tools Read,Grep,Glob` | `critique-*.md` | the lenses to apply; modify no file |
| Author (`lead = claude`: drafts or revises `problem.md` or `design.md`) | `--tools Read,Grep,Glob` | `problem.draft.md` or `design.draft.md` | output only the full artifact content; when revising, read the critique file and mark each point accept, rebut (with evidence), or defer; the host checks the draft and saves it as the artifact |
| Reviewer (`reviewer = claude`, Phase 4) | `--tools Read,Grep,Glob` | `review-rN.md` | review `diff-rN.patch` and `checks-rN.txt` against `design.md` with the Phase 4 lenses; tag severity and disposition |
| Worker (`worker = claude` or `split`, Phase 3 and `FIX` redelegation) | `--tools Read,Grep,Glob,Edit,Write,Bash` and `--allowedTools Edit Write "Bash(<test command> *)"` for each check command `design.md` names | `impl-rN.last.md` | implement `design.md` (or the listed `FIX` items) only; do not commit; list questions |

The read-only roles get no editing or shell tools, so they cannot change files or run checks; the host supplies the diff and check output as files.

## Critic

```bash
cd "$ROOT" && "$TIMEOUT" 1500 claude -p \
  "Read problem.md and verify against the codebase directly, then critique it. Keep exploration focused and finish within about 15 minutes. <lenses from the phase>. Cite file:line evidence for each point and confirm agreements briefly. Do not modify any file. User direction: <verbatim>. File: $RUN/problem.md" \
  --no-session-persistence --permission-mode dontAsk --output-format text \
  --tools Read,Grep,Glob \
  </dev/null > "$RUN/critique-problem-r1.md" 2> "$RUN/problem-r1.log"
```

## Worker

```bash
cd "$ROOT" && "$TIMEOUT" <worker_timeout_sec> claude -p \
  "Implement design.md. Make no change outside its scope. Do not commit; leave changes in the working tree. Run each listed check as one plain command from the repository root, without cd, pipes, or &&, and report the result. For anything that conflicts with the design or is unclear, do not decide on your own; list it under 'Questions:' in your final message. User direction: <verbatim>. File: $RUN/design.md" \
  --no-session-persistence --permission-mode dontAsk --output-format text \
  --tools Read,Grep,Glob,Edit,Write,Bash \
  --allowedTools Edit Write "Bash(npm test *)" \
  </dev/null > "$RUN/impl-r1.last.md" 2> "$RUN/impl-r1.log"
```

Replace `npm test` with the check commands from `design.md`.

## Claude-specific rules

- A run is successful only when the exit code is 0 **and** the output file is non-empty. A run killed by the time limit leaves the output file empty or cut off.
- `--allowedTools` patterns match whole commands, so a check wrapped in `cd`, a pipe, or `&&` is denied. Tell the worker to run each check as one plain command.
- A denied tool call does not stop the run. If the output reports that a needed command was denied, add only that command to `--allowedTools` and rerun within the rerun limit; never use `--permission-mode bypassPermissions`.
