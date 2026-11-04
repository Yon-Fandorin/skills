# Review Criteria

Apply every axis once. A section heading is not required; the behavior is.

## Contract

- The name is short enough to recall and specific enough to distinguish from neighboring skills.
- The frontmatter description states the capability and genuine trigger branches. Distinguish paraphrases of one branch from separate cases and check the boundary with plausible neighboring requests.
- Invocation policy follows the target harness and repository conventions. Do not infer explicit-only invocation from mutation; place authorization immediately before the protected action instead.
- When the package supports several hosts, each host's own policy field carries the same invocation intent (for example `disable-model-invocation` in `SKILL.md` for Claude Code and `policy.allow_implicit_invocation` in `agents/openai.yaml` for Codex). A host ignores the other host's field, so setting only one leaves the skill auto-invocable on the other.
- Inputs, output, stopping point, and non-goal agree across `SKILL.md` and any present UI metadata or catalog text.

## Focus

- The skill encodes one useful habit or one coherent workflow.
- Adjacent planning, implementation, review, and hardening work stays outside unless the skill intentionally orchestrates those stages.
- Every sentence changes likely agent behavior; exposition the model already knows is absent.

## Sources And Pointers

- Repository files, manifests, command help, schemas, and directory layout remain the source of truth for facts that are cheap to inspect.
- The skill stores conventions, reasons, edge cases, and procedures that the environment does not reveal reliably. Gotchas come from observed failures or established conventions; one task's incidental detail does not become a universal rule.
- Every reference loaded during task runs has a pointer that states what it contains and the branch that loads it. A maintainer-only file states that role at its top instead.
- Material every run needs stays in `SKILL.md`; branch-only material sits behind a pointer.
- One meaning has one authoritative location. Pointers summarize triggers rather than duplicate the target.

## Execution

- Steps use direct actions in the order the agent should perform them.
- Each step ends in a checkable completion condition.
- Approval gates appear immediately before the decision or mutation they protect.
- The workflow reaches a terminal state without implied continuation or hidden required work.

## Prose

- Leading words carry stable concepts and remove repeated explanations.
- Positive target behavior is the default phrasing; hard prohibitions pair with the behavior to perform instead.
- Definitions, rules, and caveats for one concept are co-located.
- Examples clarify a decision that prose alone leaves ambiguous.

## Packaging

- Directory name and frontmatter name agree with any present UI metadata, invocation prompt, and catalog entry.
- Direct links resolve, optional resources are routed, and no scaffold placeholders or empty directories remain.
- Scripts, hooks, assets, and persistent state each serve a concrete workflow need. Optional mechanisms are not mandatory package contents, and host-specific features must match the declared environment.
- The package does not silently depend on another skill, tool, account, or network source.

## Validation Evidence

- Match evidence to the claimed value: added capability needs evidence of task success; an encoded preference needs evidence that the workflow follows the user's process and constraints.
- Triggering evidence covers representative requests, paraphrases, and plausible near-misses. Reading the description is a static check, not a measured trigger test. Automatic triggering is not applicable to explicit-only skills.
- Functional checks measure observable artifacts, state changes, and relevant failure cases. Matching instruction wording or headings alone does not establish correct behavior.
- Each reported run identifies the tested snapshot, inputs, model and host, expected outcome, and actual output or state. Distinguish directly observed results, supplied reports, failures, partial runs, and unexecuted checks.
- Claims of improvement use comparable tasks, fixtures, models, and hosts against no skill or the previous version, as appropriate. Independent contexts reduce contamination. Without a relevant baseline, report observed performance without claiming an improvement caused by the skill.
- Scale the follow-up to the missing evidence and task risk. A few representative cases can be enough to start. Missing benchmarks are not an automatic defect in a structural review; keep them visible as evidence limits. Treat suspected no-ops or wording improvements as hypotheses until behavior supports the claim.

## Outcome

- Success is observable through a completion criterion, output contract, or a short “working if” signal.
- A reviewer finding carries evidence and impact; an implementation step names meaningful verification.
- A delegated review records its inspected scope, actual source reads, independence mode, and unfinished checks so readiness can be assessed from evidence.
- The skill stops when its own job is complete instead of absorbing the next workflow stage.

## Severity

- **Major:** likely wrong invocation, skipped required branch, contradictory authority, unsafe or incomplete workflow, broken package link, or an output that cannot satisfy the declared capability.
- **Minor:** local ambiguity or maintenance cost that does not prevent the declared workflow from completing correctly.

Cosmetic preference, hypothetical scale, and an alternative that is merely different are not findings.

## Authoring Sources

These sources inform the criteria; their tool-specific mechanics do not override the target host or user intent. Consult the original when a finding depends on a source-specific recommendation.

- [AI Hero: writing-for-agents](https://www.aihero.dev/skills-writing-for-agents): context pointers, pruning, information hierarchy, and completion criteria. Read the source selected by the exemplar reference for calibration.
- [Anthropic: Lessons from building Claude Code](https://claude.dev/blog/lessons-from-building-claude-code-how-we-use-skills/): observed gotchas, focused workflows, and optional supporting mechanisms.
- [Anthropic: Improving skill-creator](https://claude.com/resources/articles/improving-skill-creator-test-measure-and-refine-agent-skills): workflow fidelity, triggering, independent evaluations, and baseline comparisons.
- [Anthropic: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): minimal instructions grounded in representative tasks and iterative evidence.
