# Exemplar Skills

Use the [AI Hero skill catalog](https://www.aihero.dev/skills) by Matt Pocock as the default calibration set. These are exemplars, not authorities over the target skill's user intent or repository rules. Match the target's type before comparing it.

Use this map to select sources, then read the actual writing source and the matching exemplar. Compare their patterns with the target; user intent and repository rules retain authority.

## Primary Writing Reference

### `writing-for-agents`

Read the source for every target when judging context pointers, information hierarchy, co-location, completion criteria, pruning, and environment-as-source-of-truth discipline. For Agent Skills, also read its linked `SKILL-MECHANICS.md`.

- Guide: https://www.aihero.dev/skills-writing-for-agents
- Source: https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md

## Type Matches

### Recipe — `implement`

Use for a short ordered workflow whose input is already decided. It demonstrates how little prose a recipe needs when prerequisites and neighboring stages have clear owners.

- Guide: https://www.aihero.dev/skills-implement
- Source: https://github.com/mattpocock/skills/blob/main/skills/engineering/implement/SKILL.md

### Reference — `tdd`

Use for a reusable body of rules applied inside another workflow. It demonstrates a narrow trigger, explicit test seams, observable “working if” signals, and substantial detail held under one coherent habit.

- Guide: https://www.aihero.dev/skills-tdd
- Source: https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md

### Reviewer — `code-review`

Use for skills that inspect an artifact and return findings. It demonstrates fixed inputs, independent review axes, evidence requirements, explicit preconditions, and a bounded report. Borrow the independence pattern when useful; its diff-only inputs, code smells, and tracker setup belong to code review.

- Guide: https://www.aihero.dev/skills-code-review
- Source: https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md

### Router — `ask-matt`

Use only for skills whose output is the next skill or workflow path. It demonstrates branch recognition, neighboring-skill discrimination, and stopping after the route instead of starting the routed work.

- Guide: https://www.aihero.dev/skills-ask-matt
- Source: https://github.com/mattpocock/skills/blob/main/skills/engineering/ask-matt/SKILL.md

## Calibration Rules

- Compare contract shape and behavior, not tone, wording, heading names, or line count.
- Treat invocation metadata as harness-specific; never transfer it from an exemplar without a matching local rule.
- Use one matching type exemplar; a hybrid skill may use two only when both roles are explicit in its contract.
- Read the writing source and selected exemplar before completing calibration. Read their linked references only where a comparison depends on them.
- Record source URLs and the revision or retrieval date. A supplied local snapshot with known provenance is acceptable; identify it as that revision rather than claiming it is the latest.
- When a required source cannot be read, keep local findings and mark calibration incomplete. Use `Review incomplete` until the required comparison is complete.
- Treat upstream changes as new evidence, not an automatic requirement to rewrite local skills.

Source map checked on 2026-10-12 against `mattpocock/skills` at `49dd158d1076134a641b33efb035946536778336`. Select the source for each new review; this map is not a substitute for reading it.
