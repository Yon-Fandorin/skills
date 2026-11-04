# Dual Agent profile

The repository-root `.dualagent.toml` sets the roles, gates, and limits for this skill. The file is optional; without it the skill uses the defaults below.

## Resolution order

Earlier sources override later ones. A value not set by a source falls through to the next, and the defaults fill the rest.

1. **The current request**: invocation options (`--gates`, `--lead`, ...), a `direction:` instruction (`방향:` is accepted as an alias), and decisions the user changes during the run
2. **Repository authorities**: approval, branch, and commit rules in `AGENTS.md` or `CONTRIBUTING.md`
3. **`.dualagent.toml`**: the repository profile
4. **Defaults**: the table below

A request applies to **that run only** and does not change the profile file. If the user says "from now on", ask whether to save it to the profile, then save.

## Settings

```toml
version = 1

[roles]
lead = "claude"        # drafts the problem definition and design
worker = "codex"       # implements
reviewer = "auto"      # reviews

[gates]
problem = "ask"        # after the problem definition is agreed (only when the debate ran)
design = "ask"         # after the design is final, before implementation
commit = "ask"         # after the completion predicate holds, before committing

[workflow]
problem_debate = "auto"   # whether to run the problem-definition debate
debate_rounds = 2         # round limit for problem and design debate
review_rounds = 3         # round limit for review and rework
worker_timeout_sec = 1800 # time limit for one implementation run
```

| Key | Values | Default | Meaning |
|---|---|---|---|
| `roles.lead` | `claude` `codex` `user` | `claude` | `claude`: Claude drafts, Codex critiques. `codex`: Codex drafts, Claude critiques. `user`: the user gives the direction and both models refine within it |
| `roles.worker` | `codex` `claude` `split` | `codex` | `split`: Claude takes the parts that hinge on design judgment, Codex the rest. State the split in `design.md` |
| `roles.reviewer` | `auto` `claude` `codex` | `auto` | `auto`: the model opposite the worker. With `split`, each reviews the other's part. If the user picks the author's own model, state the limitation in one line and follow it |
| `gates.problem` | `ask` `auto` | `ask` | see the gate summary in SKILL.md |
| `gates.design` | `ask` `auto` | `ask` | see the gate summary in SKILL.md |
| `gates.commit` | `ask` `auto` `never` | `ask` | see the gate summary in SKILL.md |
| `workflow.problem_debate` | `auto` `always` `never` | `auto` | `auto`: run when the request is ambiguous or large (roughly four or more files, or an unknown cause); skip when small |
| `workflow.debate_rounds` | 1-4 | 2 | |
| `workflow.review_rounds` | 1-5 | 3 | |
| `workflow.worker_timeout_sec` | 300-3600 | 1800 | |

An `auto` gate means "do not ask for approval", not "skip verification or review". The conditions that stop the run under every setting are defined once, in the Exceptions row of the gate summary in SKILL.md. `auto` does not approve new product, security, or ownership decisions. Push and open pull requests only when the user asks separately, whatever the settings.

## Invocation options (this run only)

| Option | Effect |
|---|---|
| `direction: <instruction>` (alias `방향:`) | Direction, constraints, preferences. Record it verbatim under User direction and use it as a standard in every phase |
| `--lead` / `--worker` / `--reviewer` | Override `roles.*` |
| `--gates on` | Every `gates.*` becomes `ask` |
| `--gates off` | `gates.problem` and `gates.design` become `auto`, `gates.commit` becomes `never` |
| `--gates problem,design,commit` | The listed gates become `ask`; the others become `auto` (commit becomes `never`) |
| `--commit ask\|auto\|never` | Override `gates.commit` |
| `--rounds <debate>,<review>` | Override the round limits |
| `--debate always\|never` | Override `workflow.problem_debate` |
| `--phase problem\|design\|implement\|review` | Run only that phase and stop after it (no later phase, no commit). Finds the existing `.planning/dual-agent/<slug>/` directory and stops if a prerequisite artifact is missing |
| `--mode <preset>` | A preset below. Individual options passed with it win |

| `--mode` | Settings | Use |
|---|---|---|
| `default` | the profile or defaults unchanged | normal |
| `codex-heavy` | lead=codex, worker=codex, reviewer=claude | Codex leads design and implementation; Claude critiques and reviews |
| `claude-heavy` | lead=claude, worker=claude, reviewer=codex | Claude designs and implements; Codex is the independent reviewer |
| `autopilot` | `--gates off` | run to the end without approvals; no commit |
| `careful` | all gates `ask`, `problem_debate=always`, rounds 3 and 3 | large or risky changes |

## First use

When a run starts and the repository root has no `.dualagent.toml`, stop at Phase 0, before Phase 1 starts, and set up the profile. Ask for the role split and the three gates together, explain `ask` and `auto` in one line each, and show the defaults as the suggested answer.

- Write `.dualagent.toml` with `version = 1` and the keys the user chose. Keys left unchosen are not written and fall through to the defaults. If the user accepts the defaults as a whole, write only `version = 1`; the file's existence keeps the setup from running again.
- If the user declines to save, create no file, continue with the defaults, and do not ask again in the same conversation.
- When the user explicitly asks to configure the skill (for example "set up dual-agent"), run the same procedure whether or not a profile exists, and finish with the resolved values, the files changed, and the settings left at defaults.
- Write the profile only when the user approved the setup or the current task explicitly changes it. Do not search other projects for preferences to copy.
- The user decides whether to commit the profile. If it is a personal preference, offer to add it to `.git/info/exclude`.

## Validation

When reading the profile, do not guess at an unknown key or a disallowed value. Treat only that key as its default and list which key was ignored and why at Phase 0. If the whole file is not valid TOML, proceed with the defaults and tell the user. If `version` is newer than the known value, use the known keys and say so.
