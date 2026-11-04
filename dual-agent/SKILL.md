---
name: dual-agent
description: >-
  Run a code change as a two-agent workflow: Claude and Codex split design,
  implementation, and cross-model review under configurable roles and approval
  gates. Runs from Claude Code or Codex CLI.
disable-model-invocation: true
argument-hint: "[--option] <task> [direction: <instruction>]"
---

# Dual Agent

Deliver a code change by splitting design, implementation, and review across two different agents, so that by default the model that wrote a change is not the one that approves it.

Invoking this skill is the user's choice of this workflow. Run every phase the resolved settings enable, even for a one-line change; only `problem_debate = auto` may skip Phase 1, and the design critique and the Phase 4 review always run. If a single agent looks enough, say so once in the report, but do not skip phases or implement alone on that ground.

## Host and roles

- **The host is the agent that runs this skill: Claude Code or Codex CLI.** Roles assigned to the host's own model run in the host session. Roles assigned to the other model, the counterpart, run through its CLI as described under "Counterpart calls".
- Roles come from settings and name models, not hosts: `roles.lead` drafts the problem and design, `roles.worker` implements, `roles.reviewer` reviews. The default under either host is Claude as lead and reviewer, Codex as worker.
- **By default the author and the reviewer are different models.** Claude reviews what Codex wrote; Codex reviews the designs and code Claude wrote. If the user sets `roles.reviewer` to the author's own model, follow it and report the limitation.
- With `roles.worker = split`, Claude implements the parts that hinge on design judgment and Codex the rest. Otherwise the worker implements everything assigned to it.
- With `roles.lead = user`, the user's direction is the starting point. Claude writes the artifact and Codex critiques it, as with `lead = claude`.
- Pass state between agents through files, not conversation. Conversation context is volatile.
- Other skills loaded during the run follow this skill's gates. Hold their setup questions until the run ends.
- Push and open pull requests only when the user asks separately.

## Settings

At Phase 0, read [references/profile.md](references/profile.md) and resolve settings in its resolution order (the current request first, defaults last).

**Any value the user does not set falls through to the profile, then to the default.** Treat the profile and repository authorities as read-only unless the user accepts the first-use setup or the task explicitly changes them.

### User direction

Record a `direction:` instruction (for example "keep the existing API", "minimal change", "readability over performance") verbatim under **User direction** in `problem.md`. Include it in every counterpart prompt and in the review criteria. If the problem definition or design conflicts with it, report the conflict instead of changing it silently.

### Mid-run changes

- At every gate the user may redirect instead of approving. Update the affected artifact and mark later stages that depend on it as stale (a direction change during design invalidates the critique already received).
- If the direction changes during implementation, do not wait for the running worker to finish. Confirm whether to stop it, then update `design.md` first.
- Append the new direction with its point in the run. Do not overwrite earlier directions.
- A setting changed mid-run applies to this run only. Ask before saving it to the profile.

## Working directory

Use `.planning/dual-agent/<slug>/`, where `<slug>` is a short kebab-case summary of the task:

| File | Content |
|---|---|
| `baseline.txt` | `git status --porcelain` at the start of the run |
| `problem.md` | symptoms, evidence, hypotheses, constraints, non-goals, user direction |
| `design.md` | approach, files to change, acceptance criteria, test plan, role split |
| `*.draft.md` | a counterpart author's draft before the host saves it as the artifact |
| `critique-*.md` | the counterpart's critiques (problem-r1, design-r1, ...) |
| `impl-rN.log`, `impl-rN.last.md` | implementation log and final message |
| `diff-rN.patch` | the full change under review in round N |
| `checks-rN.txt` | output of the tests, linter, and type checks the host ran in round N |
| `review-rN.md` | review findings and their dispositions |
| `summary.md` | final summary |

Define `ROOT` as the repository root (`git rev-parse --show-toplevel`) and `RUN="$ROOT/.planning/dual-agent/<slug>"`. Use `"$RUN"` for every artifact, output file, and log redirection: the shell resolves redirections before the CLI starts, so pointing the CLI at `$ROOT` alone does not protect relative paths when the run starts in a subdirectory. If `.planning/` is not ignored by Git, create `.planning/.gitignore` containing `*` (the file ignores itself, so no tracked file changes) and mention it in the report; if `.planning/` already holds tracked files, put that file in `.planning/dual-agent/` instead. Never commit `.planning/`; raw CLI logs there can hold sensitive command output.

## Counterpart calls

Read the call reference for the current host before the first counterpart call. It defines the critic, author, reviewer, and worker shapes:

- Claude Code host: [references/codex-calls.md](references/codex-calls.md) (`codex exec`)
- Codex host: [references/claude-calls.md](references/claude-calls.md) (`claude -p`)

Rules for every call:

- Always add `</dev/null` and `"$TIMEOUT"` (Phase 0). Without them a run can wait for input and hang. A repository-wide critique can take well over ten minutes, so give critique calls a generous limit (about 1500 seconds) and ask the counterpart to bound its own exploration.
- Some hosts start a new shell for every command (Claude Code does), so define `ROOT`, `RUN`, and `TIMEOUT` in the same command as the call, or write their resolved values into it.
- Run a call in the background when its time limit exceeds the host's foreground command limit (10 minutes in Claude Code; check the host's own limit otherwise), and check the success condition only after it exits.
- Redirect output to files and read only the needed lines with `tail` or `grep`, so the host context stays small.
- Include the user direction verbatim in every prompt.
- Treat a run as successful only under the success condition in the call reference. Otherwise read the log and report failure. Do not simply retry the same command.
- Answer the worker's "Questions:" from the design and rerun when you can; otherwise ask the user. Rerun at most twice per chunk, and stop and ask the user if the same question recurs.
- A counterpart call sends repository content to the other vendor's service under the user's login, and invoking this skill is the request for it. When the host asks for approval to run a call, state the destination, the files the prompt points to, and the purpose. If the host or its approval review rejects the call, stop, explain the rejection, and ask the user to approve sending repository content and this run's artifacts (problem, design, critiques, diff, check output) to the counterpart for this run; an approval review reads the scope literally, so name all of them. Cite that approval in later requests instead of asking again.
- Never bypass the counterpart's sandbox or permission checks.

## Phase 0. Preconditions and settings

1. Identify the host. Check that the counterpart CLI exists (`codex --version` under Claude Code, `claude --version` under Codex) and that `timeout` or `gtimeout` exists (stock macOS has neither). Set `TIMEOUT` to the one found. If either is missing, stop and say so. Set `ROOT` to the repository root.
2. In a new run, first create `$RUN` and make sure `.planning/` is ignored (see "Working directory") so the run's own files stay out of the baseline. Then record the initial `git status --porcelain` (staged, unstaged, untracked) in `$RUN/baseline.txt` so later phases can tell task-owned changes from pre-existing ones. A `--phase` run reuses the existing `baseline.txt` and never overwrites it. Do not stop here for the current branch or for uncommitted changes: Phase 5 handles a commit on `main` or `master`, and Phase 2 stops only if the design touches a file with pre-existing changes.
3. Resolve the settings. Check for the profile with `test -f "$ROOT/.dualagent.toml"` (a dotfile that a plain `ls` hides), read it when it exists, and report any validation problems in this phase. Treat the profile as missing only when that check fails.
4. When `workflow.problem_debate = auto`, judge the size. Skip Phase 1 if the request is clear and the change is small.
5. **Phase selection and unclear settings.** With `--phase`, the run covers only the named phase and **stops after it**: the normal transition to the next phase (including an `auto` design gate) and Phase 5 commit handling do not apply. Look for the existing `.planning/dual-agent/<slug>/` directory (ask which one if several match), and stop if a prerequisite artifact for the requested phase is missing (`baseline.txt` for every phase, and for example `design.md` for `implement`). In a normal run, do not print the resolved settings and do not ask for confirmation. Stop and ask only when something is unclear: an option or direction that can be read two ways, settings that conflict across sources, or a missing prerequisite; show only the unclear items and where each value came from. If no profile exists, run the first-use setup in the profile reference before Phase 1; it is the one start-of-run question in a normal run.

## Phase 1. Problem-definition debate (when `problem_debate` applies)

Goal: both models agree on the real problem, not the symptom.

1. The lead investigates the codebase (delegate wide exploration when the host supports it) and writes `problem.md`; a counterpart lead uses the author shape. With `lead = user`, start from the user's direction and let both models refine it.
2. The other model critiques it **read-only** with these lenses: (1) is this a symptom or a root cause, (2) unverified assumptions, (3) alternative interpretations missed, (4) missing constraints or non-goals. When that model is the counterpart, use the critic shape.
3. The lead resolves each point as **accept / rebut / defer** and updates `problem.md`, giving evidence when rebutting and not conceding without it. A counterpart lead does this through the author shape, given the critique file; the critic never rules on its own critique.
4. If disagreement remains, run another round, up to `workflow.debate_rounds`. If it still remains, summarize both positions and let the user decide.
5. **Gate: `gates.problem`**, as defined in the gate summary.

## Phase 2. Design

1. The lead writes `design.md`: approach, files to change, verifiable acceptance criteria, test plan with the check commands, and what is out of scope. With `worker = split`, state the split.
2. The other model critiques the design read-only, up to `workflow.debate_rounds`, with these lenses: does the design meet the acceptance criteria, a simpler alternative, risk and regression, missed edge cases.
3. The lead resolves the critique and finalizes `design.md`, as in Phase 1 step 3.
4. If `design.md` changes a file that `baseline.txt` lists with pre-existing changes, stop and ask how to handle that file, whatever the gate settings.
5. **Gate: `gates.design`**, as defined in the gate summary.

## Phase 3. Implementation

Follow `roles.worker`. When the worker is the host's model, the host implements in its session. When it is the counterpart, use the worker shape. With `split`, follow the split in `design.md`. The resolved reviewer is the model opposite the implementer unless `roles.reviewer` is set explicitly.

For large work, split it into independent chunks of about 25 minutes or less and run a separate worker call per chunk.

## Phase 4. Review, discuss, redelegate

Run up to `workflow.review_rounds` rounds. Each round:

1. Prepare. The host writes the whole change to `$RUN/diff-rN.patch`, not only unstaged edits: `git diff HEAD` (staged and unstaged) plus the contents of task-owned untracked files from `git ls-files --others --exclude-standard`, excluding what `baseline.txt` shows as pre-existing. The host runs the tests, linter, and type checks that exist and saves their output to `$RUN/checks-rN.txt`.
2. Review. The reviewer is the model that did not implement, unless `roles.reviewer` names another; never hand the review to the implementer's model on your own. With the defaults (worker = codex) the host Claude reviews in its own session. The reviewer compares the change with the acceptance criteria in `design.md` and the check output, and looks for scope drift, omissions, bugs, regression risk, test gaps, and violations of the user direction. A counterpart reviewer uses the reviewer shape and names any check it could not judge.
3. Record each finding in `review-rN.md` with a **severity** (CRITICAL, WARNING, INFO) and a **disposition**:
   - `FIX`: must change; redelegate to the worker
   - `NO-CHANGE`: not a problem or an intended change (give the reason)
   - `OPEN`: undecided; needs discussion
4. Discuss. For `OPEN` findings or ones the reviewer is unsure about, ask the implementer read-only for its position (why it was done this way, what alternatives it considered); a counterpart implementer answers through the critic shape. Change the disposition when it gives a valid reason. Do not concede without one.
5. Redelegate only the `FIX` items. Pass `review-rN.md` as a file, restrict the worker to those items, and forbid other changes. Then start the next round, which reviews the updated change.
6. **Completion predicate** (used here, in Phase 5, and in "Done when"): the acceptance criteria are met, the latest review pass has no CRITICAL finding and no unresolved `FIX` or `OPEN` item, and the final diff was reviewed after the last change. The loop ends only when this holds.
7. Escalate. If the limit is reached without the predicate (including fixes made in the last round that no review pass has seen), the same finding keeps recurring, or the two models are deadlocked, stop **regardless of gate settings**, report the outcome as incomplete with the state, the dispute, and the options, and do not commit automatically. A broken design premise is a likely cause, so also offer to return to Phase 2.

The reviewer may edit directly only for trivial fixes (typos, comments, formatting). Record each such edit in `review-rN.md` and rerun the affected checks. Redelegate anything else, so the author's counterpart still sees every behavioral change.

## Phase 5. Wrap-up

1. Write `summary.md`: changed files, per-round review results, remaining issues (INFO and unresolved), and the checks that ran, separating passed, failed, and not run.
2. **Gate: `gates.commit`**, as defined in the gate summary.
3. **Commit boundary.** On `main` or `master`, commit on a new branch `dual-agent/<slug>` instead (with `ask`, propose the branch with the commit). Stage only reviewed, task-owned paths by name (never `git add -A` or `git add .`), leave anything `baseline.txt` marks as pre-existing or already staged out of the commit, and exclude `.planning/`. Show the staged path list before committing.

## Gate summary

This table is the single definition of gate behavior.

| Gate | When | Setting | `ask` | `auto` | `never` |
|---|---|---|---|---|---|
| Problem | end of Phase 1 (when it ran) | `gates.problem` | show the agreed problem definition; wait for approval | show a summary; continue | - |
| Design | end of Phase 2, before implementation | `gates.design` | show a summary of `design.md` and the remaining disagreements; implement only after approval | show the same; implement | - |
| Commit | Phase 5 | `gates.commit` | show the final diff summary and remaining issues; commit after approval | commit when the completion predicate holds and no known rule violation remains; report | leave changes in the working tree; report the diff summary |
| Exceptions | round limit exceeded, deadlock, execution failure, direction conflict, a question the design cannot answer, unclear settings at Phase 0, first-use setup when no profile exists, pre-existing changes in a file the design changes | - | **always stop, whatever the settings** | | |

## Reporting and failures

- When reporting, separate what was verified from what was not. Do not relay the counterpart's output unverified.
- If a counterpart call fails (authentication, timeout, sandbox or permission error), report the cause. Do not switch to single-agent work on your own; ask first.
- Do not edit `.dualagent.toml` or repository authorities unless the user asked.

## Done when

- every phase that the resolved settings enable has run, and each gate was handled as configured;
- the review loop ended with the completion predicate holding, or the incomplete outcome was escalated to the user;
- `summary.md` states the outcome, the checks that ran, and the unresolved issues;
- no commit, push, or pull request happened beyond what `gates.commit` and the user allow.
