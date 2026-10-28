# Software projects

Use for scopes whose maintained deliverable is software. Inspect approved
ownership, representative consumers, build configuration, contribution docs,
and meaningful tests. Apply language-specific conventions only to the code
surfaces they govern.

When contribution guidance is requested, ground it in the actual change
workflow: responsibility boundaries, preserved behavior and compatibility,
relevant validation, and any established review or release constraints. Prefer
maintained command and configuration sources to duplicated lists. Missing tools
or rules do not justify creating a generic development policy.

## Requested software work

Guidance authoring alone does not start implementation. For requested code
changes or scoped code review, load `codewright` and follow its applicable
references and approval settings. For responsibility, placement, public API,
or dependency decisions, first load `codebase-architecture`.

Pass the agreed structure contract, affected paths, and preserved behavior to
Codewright. Reopen design only for a concrete contradiction or a new
responsibility outside the contract. After implementation, verify applicable
checks and the final diff, then trace imports, exports, construction sites,
consumers, and the affected common parent against the contract. Report structural
review separately from compiler and behavior results. A design-only request
ends with the contract.

If a needed skill is unavailable, state the limitation and use applicable
repository rules; identify any verification or decision left unresolved.
