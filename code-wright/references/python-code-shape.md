# Python Code Shape

Use nearest comparable repository code to select conventions. A refactor changes maintainers' work while preserving the consuming interface.

## Mapping Contracts

When callers repeatedly reconstruct a stable mapping's required keys or nullable values, make that contract explicit using the repository's existing model conventions. `TypedDict` can document a dictionary without replacing its runtime representation; an existing dataclass, validation model, or named interface may already express the contract. Reuse a suitable existing shape before adding another.

Keep unvalidated input distinguishable from normalized values at the boundary that owns validation. Follow the repository's existing input and validation model; adding annotations does not authorize a representation or validation migration. Leave genuinely dynamic mappings generic.

## Expression And Ownership

Keep validation, normalization, and storage operations distinguishable. A named intermediate earns its place when it exposes a decision or invariant obscured by precedence, repeated lookup, or a nested conditional. Preserve evaluation order, strict type checks, empty-value policy, and exception behavior.

Compare a proposed helper with its current callers. Similar SQL syntax alone does not make distinct domain conflict policies the same responsibility.

When considering a persistence abstraction, inspect transaction semantics, returned value shapes, resource lifetime, and exception ownership before reuse. Match the existing contract or leave distinct policies local; syntactic duplication alone does not justify changing storage behavior.

## Refactor Check

Trace changed shapes through every consumer. Verify the applicable consuming contracts through existing public-interface tests, including serialization or error behavior when affected. A typing-only change can be verified by the repository's existing static gate when present; adding a checker solely for this refactor is outside this reference.

Source: [Python TypedDict](https://docs.python.org/3/library/typing.html#typing.TypedDict). The choice of owner and contract remains repository-specific.
