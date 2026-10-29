---
name: codebase-architecture
description: >-
  Design or review codebase structure: public entry points, responsibility owners,
  module placement, and dependency boundaries. Use when organizing a codebase,
  separating protocols from domain concepts, or evaluating whether a refactor
  creates real layers rather than moving files. Reuse settled architecture
  decisions. Not for routine implementation or deployment topology design.
metadata:
  version: "1.0.0"
---

# Codebase Architecture

Decide where responsibilities belong and which dependencies are allowed. Produce
the smallest structure contract an implementer can follow. Work with the actual
language and repository; no default Clean Architecture, DDD, directory taxonomy,
or one-module-per-type rule.

## Start from settled decisions

Read repository instructions and the user's architecture choices before proposing
structure. An approved direction is input to apply, not a question to reopen.
Do not require new usage examples, an interview, alternatives, or a design document
when the existing request and code settle the relevant choices. Resolve ordinary
placement decisions autonomously. Ask only when a material ownership, behavior,
or compatibility conflict cannot be resolved from the available authority.

Treat current placement as evidence, not as proof that it is the intended
architecture. Distinguish declared constraints from historical accidents. A
suggested architecture is a proposal until adopted; do not silently promote a
prior suggestion or an inferred dependency rule into a requirement.

Design and review are read-only by default. Implement only when the user's request
also authorizes implementation. A design task does not authorize rewriting
history, changing other skills or settings, publishing, or deploying.

## Inspect the boundary being decided

Trace the affected entry points through policy, contracts, and concrete effects.
Read implementations, construction sites, exports, and real consumers; file names
and successful compilation do not establish ownership. Include the common parent
and siblings needed to decide placement. Record coverage and mark uninspected
areas when the requested review is broader than the evidence obtained.

Keep these distinct:

- **Public namespace:** how consumers find and call the capability.
- **Responsibility owner:** where its decisions, invariants, and state live.
- **Physical placement:** source files, directories, packages, or crates.
- **Dependency direction:** actual imports/types and permitted knowledge.
- **Runtime flow:** calls, callbacks, events, and composition wiring.

Draw dependency arrows with a named meaning. A runtime response traveling back to
a caller does not by itself reverse the source dependency. A public re-export
does not require keeping the old physical file. A new folder does not establish
a dependency boundary.

## Choose ownership and placement together

Use observed consumers, shared changes, independent policies, state lifetimes,
and dependency direction to choose an owner. Distinguish Git change history from
an inferred change scenario. Cite concrete code when reporting a structural flaw;
numbers, prefixes, or line counts alone are not a reason to split or group.

Group related responsibilities under a shared concept when that improves actual
navigation and expresses ownership. Keep child boundaries that protect distinct
invariants or lifetimes. Flatten forwarding-only files and one-child directories
when they have no visibility, platform, tooling, or ownership purpose. Review the
combined parent structure even if each child looks reasonable in isolation.

For each proposed boundary, identify its owner, actual consumers, shared contract,
and dependencies it permits or forbids. A layer must change what code is allowed
to know or decide, not just where it is stored. Give at least one concrete
boundary violation a reviewer could recognize.

Keep protocol representation and domain meaning separate only to the extent the
product needs. Do not invent a parallel domain model for every wire DTO. Shared
financial or business rules should not need a concrete network client; protocol
field mapping can remain with the protocol. Do not force request/response and
event/session lifecycles through one interface merely because both communicate.

Use the language's existing mechanisms first: modules, functions, types, package
visibility, exports, and composition. Add a trait, interface, facade, adapter,
mapping layer, or package only when its current callers or an explicit product
contract justify the cost. An external SDK API is a real consumer contract even
without in-repository callers. Existing dependency injection need not be removed.

When a decision involves protocol contracts or domain meaning, compatibility
exports, effectful lifetimes, shared utilities, or adapting architecture patterns,
read the relevant section of [boundary cases](references/boundary-cases.md).
Otherwise keep the pass local.

## Deliver the structure contract

Scale the result to the task. A brief explanation suffices for a settled move;
use a before/after tree and a dependency table for a substantial reorganization.
Include only what changes an implementation decision:

- Confirmed direction, affected scope, and unresolved assumptions.
- Proposed placement and the responsibility of each significant part.
- Permitted/forbidden dependencies and the actual public entry points.
- Compatibility and behavior constraints, including any necessary alias or migration.
- Structural acceptance checks and the behavior checks affected by the move.

Retain a reasonable existing structure when no evidence supports changing it.
Compare alternatives only where the decision is materially ambiguous, including
the smaller adjustment. Do not pad the output with mandatory ADRs, deferred-work
lists, hypothetical scalability, or a universal rollout plan. Save a document
only when requested or required by the repository; follow its location and
tracking rules. Follow the user's language for the explanation.

## Hand off and verify

This skill owns the structure contract. Code Wright, when available, owns scoped
implementation, code clarity, language conventions, and regression verification.
Pass it the contract, affected paths, and preserved behavior; do not require it
to rediscover approved owners. This skill also works without Code Wright: an
implementer can follow the same contract using repository rules.

Return to the structure decision only when implementation reveals a concrete
contradiction or a new responsibility outside the contract. Routine moves and
language-specific expression of settled boundaries do not restart design.

For an implemented change, trace the final imports, exports, construction sites,
and representative paths against the contract, including the whole affected
parent. Use existing visibility or dependency tools where applicable; a separate
package or custom checker is not required for every boundary. Report structural
checks separately from formatter, compiler, and behavior test results.

Finish when owners and dependency rules are explicit, the proposed structure
addresses the observed cost, compatibility obligations are accounted for, and
any remaining conflict or unverified claim is named. Do not describe a proposed
tree as implemented, green tests as architecture proof, or a self-review as an
independent evaluation.
