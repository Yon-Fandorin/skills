# CLI Project Structure

Use this contribution reference when a command-line application has command groups and leaf commands, when an existing parser/execution layout is being reorganized around those commands, or when CLI runtime orchestration, frontend/mode dispatch, or backend assembly changes. The role boundaries are the rule; filenames follow the consuming language and repository.

Before introducing or changing this hierarchy, apply **Confirm shape** in the parent skill's **Run** section. When the repository already contains an approved command hierarchy, extend that foundation without requesting the same confirmation again.

## Change Axis

A CLI usually grows by user-visible command. Arguments, execution, output, errors, and scenarios for one command tend to change together. Prefer a vertical command slice when a horizontal `model`, `parser`, and `execution` split would require every command change to touch all three files.

Keep a horizontal boundary only when another real parser, transport, generated surface, or non-CLI caller uses it.

## Baseline

The following Rust-style example contains one command group and one leaf command:

```text
src/
├── main.rs
├── application.rs
├── command.rs
└── command/
    ├── workspace.rs
    └── workspace/
        └── bind.rs

tests/
├── cli.rs
└── common/
│   ├── mod.rs
│   └── directory.rs
```

For Rust module and source unit-test filenames, follow the Rust contribution
reference. Do not rename unaffected modules solely to modernize them.

Under Cargo, each direct `tests/*.rs` file is a separate integration-test crate.
Shared helpers may live in a nested module such as `tests/common/mod.rs` or
`tests/support/mod.rs` and be imported by a test target. Nesting prevents separate
target discovery; `mod.rs` has no special test semantics. Follow an existing
repository convention when it is deliberate.

## Parent Topology

Command-owned modules normally follow the user-visible command tree. Classify
non-command support code by stable responsibility and independent change axis,
not its current filename.

A crate-root sibling is justified when it has independent ownership, genuine
reuse by multiple owners, a repository-authorized composition or entrypoint
role, or an intentional public or package surface. A single-consumer support
module is a candidate to descend under that consumer only when dependency
direction and required visibility support the move. Decompose a mixed module
before relocating its parts instead of assigning all of them to one convenient
parent.

Do not introduce `core`, `common`, or `utils` merely as umbrellas. Shortening a
directory listing is not an ownership reason. For a structural CLI proposal,
show the affected parent's before and after trees and the intended dependency
direction. This supplies the CLI-specific evidence for **Confirm shape**; the
parent skill owns approval and continuation.

## Source Ownership

- A CLI composition root owns process startup and the repository-defined top-level wiring. It may connect process-wide resources or concrete implementations when repository authority assigns that responsibility.
- When the repository has an `application` layer, it connects argument parsing, execution, output streams, error reporting, and exit status.
- the top-level command root declares and routes top-level command groups;
- a command-group root declares and routes only that group's subcommands;
- a leaf command owns its arguments, command-specific execution, and output construction;
- ordinary module entry files contain module documentation, declarations, and re-exports rather than leaf behavior;
- a crate or package root used as the composition root may contain repository-authorized top-level orchestration.

Routers delegate immediately. Leaf commands do not depend on parent routers. Avoid a second parser-neutral command model when it merely duplicates the parser types.

For Rust with Clap derive, a conventional composition is `Parser` at the top-level owner, `Subcommand` on routing enums, and `Args` on group and leaf owners.

For runtime orchestration, treat provider, frontend or presentation mode, launch or resume mode, and lifecycle phase as separate variation axes only when they can evolve independently. A composition root or shared runtime owner may coordinate one coherent lifecycle. Review a new change when adding one axis requires parallel policy branches through startup, execution, output, switching, or cleanup, or when provider-specific policy spreads into a generic owner that repository authority does not assign it.

Treat platform as a separate variation axis when it can evolve independently. Repeated platform gates across declarations, implementations, and tests may justify a repository-authorized boundary, such as a platform module or dispatcher, but repetition alone does not require restructuring. Keep local gates for narrowly platform-specific operations. Before moving a platform implementation behind a new nested boundary, preserve root-qualified imports, child-module discovery, and named test or integration entrypoints. Verify that platform predicates match the documented and validated target matrix. Broad predicates—for example, Rust's `cfg(unix)`—may include unsupported targets; report that mismatch without changing the product's support scope.

## Test Ownership

- Classify tests by the interface they exercise, not by the assertion type:
  - Keep tests in the owning source target when they require private access or isolate an internal unit, including injected collaborators or failures.
  - Put tests under the package `tests/` directory when they use only the public API or launch the built CLI as an external consumer.
- Parser behavior, stdout/stderr, exit status, and PTY behavior may be tested at either boundary; those observations alone do not determine placement.
- Keep unit tests under the narrowest production owner. Do not widen production visibility solely for tests; when a split breaks private test access, move or nest the tests with that owner, or test through the module's intended boundary.
- When several unit-test groups share `cfg(test)` under the same owner, one `#[cfg(test)] mod tests;` entry may own focused children under the matching module directory; preserve a separately gated named source module when a fixture or subprocess invokes its test-filter path directly.
- Organize integration scenarios by the command users invoke, not by parser or execution layer.
- Use a top-level integration entry file when the build tool discovers only top-level targets; nested files then hold command scenarios.
- Do not create test copies of routing files that have no behavior contract.
- Put shared fixtures under `support` only when they improve multiple scenarios.
- Treat help text, output, exit codes, and failure text as contracts when users or automation rely on them.
- Run the integration target after moving tests; a plausible tree does not prove discovery.

## Growth

Adding `workspace inspect` creates a sibling leaf file and one routing variant. Existing leaf files remain unchanged unless both commands truly share policy. A new top-level command group becomes a sibling directory with its own router.

Do not add empty command directories, placeholder leaf files, or generic utility modules for anticipated commands.

## Review Checklist

- Does the source tree follow the user-visible command tree?
- Does each leaf own the code that changes with it?
- Does every changed child of the affected parent justify remaining a sibling rather than descending under one clear owner?
- Do roots perform only repository-authorized composition and orchestration rather than unrelated policy?
- Are module entry files free of unrelated implementation?
- Does every newly cross-module item represent an intended boundary operation rather than an implementation detail made reachable by the split?
- Do tests live under the command behavior they prove?
- Did the test runner discover moved tests?
- Are output and error contracts preserved?
- For runtime changes, did an independently changing axis become coupled through shared or duplicated lifecycle policy, or introduce an unauthorized concrete dependency?
- Is platform variation localized at an existing or justified ownership boundary?
- If platform code moved, do root-qualified imports, child modules, and named test or integration entrypoints still resolve and get discovered?
- Do platform predicates match the documented and validated target matrix?
