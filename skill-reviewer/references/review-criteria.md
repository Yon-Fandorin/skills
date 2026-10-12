# Review Criteria

Apply every axis once. A section heading is not required; the behavior is.

## Contract

- The name is short enough to recall and specific enough to distinguish from neighboring skills.
- The frontmatter description states the capability and the branches that trigger it.
- Invocation policy follows the target harness and repository conventions. Do not infer explicit-only invocation from mutation; place authorization immediately before the protected action instead.
- Inputs, output, stopping point, and non-goal agree across `SKILL.md` and any present UI metadata or catalog text.

## Focus

- The skill encodes one useful habit or one coherent workflow.
- Adjacent planning, implementation, review, and hardening work stays outside unless the skill intentionally orchestrates those stages.
- Every sentence changes likely agent behavior; exposition the model already knows is absent.

## Sources And Pointers

- Repository files, manifests, command help, schemas, and directory layout remain the source of truth for facts that are cheap to inspect.
- The skill stores conventions, reasons, edge cases, and procedures that the environment does not reveal reliably.
- Every reference has a pointer that states what it contains and the branch that loads it.
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
- Scripts and assets exist only when repeated deterministic work or generated output needs them.
- The package does not silently depend on another skill, tool, account, or network source.

## Outcome

- Success is observable through a completion criterion, output contract, or a short “working if” signal.
- A reviewer finding carries evidence and impact; an implementation step names meaningful verification.
- A delegated review records its inspected scope, actual source reads, independence mode, and unfinished checks so readiness can be assessed from evidence.
- The skill stops when its own job is complete instead of absorbing the next workflow stage.

## Severity

- **Major:** likely wrong invocation, skipped required branch, contradictory authority, unsafe or incomplete workflow, broken package link, or an output that cannot satisfy the declared capability.
- **Minor:** local ambiguity or maintenance cost that does not prevent the declared workflow from completing correctly.

Cosmetic preference, hypothetical scale, and an alternative that is merely different are not findings.
