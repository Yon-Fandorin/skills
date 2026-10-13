# Boundary cases

Consult the section reached by the current decision. These are judgment criteria,
not required directories, classes, or interface patterns.

## Public entry points and compatibility

For an SDK or plugin, public paths and external extension contracts are consumers
even when repository code never calls them. Check published exports, examples,
integration tests, and applicable compatibility requirements. Absence of local
use alone does not establish dead code.

Separate canonical public paths, compatibility paths, and physical implementation
locations. Use language-supported aliases or re-exports where they preserve the
actual contract without retaining legacy implementation files. Check visibility,
type identity, constructors, extensions, and build/tooling paths as applicable;
runtime equality alone cannot prove source compatibility. If preservation is not
possible, report the exact break and seek resolution within the user's scope.

A facade is useful when it owns a coherent consumer contract or construction
policy. A wrapper forwarding every existing operation through a second identical
surface adds a maintenance cost; do not create it solely to illustrate a layer.
Composition code may know concrete adapters to assemble them without transferring
that knowledge into domain policy.

## Protocol contracts and domain meaning

An SDK's wire field names, headers, frame envelopes, and acknowledgements can
belong to its protocol contracts. A domain type or rule is useful when consumers
need transport-independent meaning, validation, or operations. Serialization
support alone does not prove that a type has the wrong owner; inspect which
protocol assumptions its rules carry.

For a user-approved REST/WebSocket separation, express distinct call and session
entry points and keep the underlying communication implementations identifiable.
Share authentication or domain rules when semantics actually match. Do not hide
an order replay policy inside a generic sender or merge a stream session's
cancellation and acknowledgement state into an HTTP request helper.

A public protocol-specific request type can coexist with shared business types.
Do not add conversion objects or a supposedly pure domain layer whose only job
is to duplicate every field. Report wire-contract preservation separately from
shared semantic invariants when a move touches both.

## State, transactions, and effectful lifetimes

Follow the owner of cancellation, deadlines, locks, transactions, acknowledgement,
retries, and cleanup before extracting orchestration. Splitting a workflow that
must be atomic can destroy its contract even if the import diagram looks cleaner.
Keep a coherent state machine with its lifecycle owner; models and codecs may be
separate without splitting the authority to mutate state.

Retain existing injection seams that make policies testable. A new seam must solve
a current caller, lifecycle, testability, or extension requirement. Deterministic
logic does not need an interface merely because it sits below an effectful caller.
Use the language's simplest adequate mechanism, including a function or callback.

## Shared support and grouping

Two callers do not automatically justify a shared utility module. Compare semantics,
change causes, and lifetimes. Similar code with independently changing rules may
be better kept with each owner. When behavior is shared, place it under the common
owner or an explicit shared contract with a deliberate dependency direction.

A repeated prefix is a signal to inspect consumers and the parent topology. Group
only if the responsibilities form a coherent concept and navigation improves.
Tests needing private access often belong with their production owner; follow
actual test discovery and local conventions rather than prescribing a test tree.

## Adapting an architecture pattern

Apply the boundary rule that addresses the problem, not a pattern's complete
reference layout. An application may need use cases; an SDK may primarily expose
protocol contracts and client/session policies; a small script may need neither.
Do not add repositories to code with no persistence or choose services because
a design guide uses them in its examples.

Translate decisions through the target language and build system. In Rust this
may use module visibility and re-exports; in other languages it may use package
exports, access modifiers, or conventions backed by dependency tooling. Keep
language syntax out of the general ownership rule. Treat repository-authorized
mechanisms as constraints, not inferior versions of another language's idiom.
