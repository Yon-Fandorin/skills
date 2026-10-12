# TypeScript And React Code Shape

Use existing compiler settings and nearby feature code as the style authority. Name the maintenance cost a change removes; reduced line count alone is not a design result.

## Request And Type Ownership

Before creating a client wrapper, inspect existing request owners and their observable policies. Share mechanics when current callers' obligations decrease enough to justify the added interface and coupling. Different decoding, authentication, cancellation, or error contracts may warrant separate clients; compare the cost of a policy adapter with keeping those clients local. Keep independently changing protocol decisions with their owners.

Make consumed shapes explicit when an envelope dependency forces callers to provide unrelated data or obscures a stable contract. Reuse existing types first. Indexed access, `Pick`, or a named shape are alternatives; choose the one that expresses the intended dependency with the least duplication. A new name alone is not a reduction in coupling.

Keep assertions at the boundary they represent. Replacing assertions with validation, changing error fallback, or narrowing accepted payloads changes behavior and belongs in an explicitly authorized behavior change.

## React Composition

Distinguish workflow orchestration, pure transformations, and repeated presentation. Keep an effect with the state and lifecycle it owns. A custom hook earns a separate interface when it hides a cohesive stateful operation from an actual consumer, not when it merely moves lines out of a long component.

A view extraction should keep render inputs and event callbacks small, and leave transport policy with the workflow. Reuse presentation logic when real consumers share an output contract; a wrapper earns its place by hiding an actual caller obligation.

## Refactor Check

Verify affected request methods, headers, payloads, decoded results, and error messages remain equivalent. Run the existing TypeScript/build gate, then inspect affected UI actions and states in the browser. Compare external behavior rather than testing helper names or the new file layout.

Sources: AI Hero [codebase-design](https://www.aihero.dev/skills-codebase-design) for deletion, interface, and locality tests; [TypeScript indexed access](https://www.typescriptlang.org/docs/handbook/2/indexed-access-types.html) for shape dependencies.
