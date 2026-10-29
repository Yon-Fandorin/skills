---
name: project-guide
description: >-
  Assess a project's purpose and working practices, then establish or refine its
  agent instructions, contribution guidance, and management conventions. Use for
  project guidance and setup. Delegates AGENTS.md authoring to agents-writer;
  routine code changes belong to Code Wright.
---

# Project guide

## Assess the project

Read the user's request, applicable instructions, maintained project docs, and
representative artifacts and workflows. Identify what the project produces,
who maintains it, and what the requested guidance covers. Distinguish explicit
policy from inferred practice. A script, code example, or tool configuration
alone does not establish that the project is software development.

Reuse supported assessments and approved decisions. Mixed projects may need
different guidance for different areas; assess the affected scope rather than
forcing one repository-wide type.

## Select applicable guidance

Consult [project types](references/project-types.md) and read only guides whose
conditions match the evidence. Apply existing authoritative contribution rules
where they govern, regardless of the inferred type.

If the project uses Git, read [Git workflow](references/git-workflow.md) for
draft PRs and explicit CI/CD opt-in. Carry these rules into requested project
instructions. Git usage alone does not select the software project type.

When the type is uncertain or has no guide, keep supported common rules and
omit unsupported type-specific additions. State the uncertainty. Ask a focused
question only when the answer is needed to complete a requested decision;
otherwise finish the grounded portion without inventing contribution policy.

## Establish the requested conventions

Use the assessment and matching guide to identify actual ownership, maintenance
workflow, sources of truth, and meaningful validation. Preserve established
rules; propose changes only where the request and evidence justify them. Keep
contribution instructions proportional to how this project is maintained.

For requested `AGENTS.md` creation, revision, or review, load `agents-writer` and
pass the scope, evidence, approved rules, selected type guidance, and unresolved choices.
It owns wording, placement, and instruction verification. If unavailable,
report that limitation; an assessment alone does not complete instruction
authoring.

Edit only requested management documents or perform explicitly requested work.
An assessment does not authorize creating contribution files, changing code or
configuration, or extending this skill's catalog. Keep detailed procedures with
their owners and use conditional pointers where project instructions need them.

## Completion

For produced or revised deliverables, follow
[fresh-context review](references/completion-review.md) before claiming
completion. The final snapshot must have no unresolved actionable findings;
an unavailable or unfinished required review leaves the work incomplete.
Carry this completion criterion into requested project working instructions.

Report the supported project assessment, resulting conventions or changed
files, verification, final review result, and unresolved decisions. Separate
observed practice, adopted policy, and unaccepted recommendations.
