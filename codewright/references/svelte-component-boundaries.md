# Svelte Component Boundaries

Read when changing Svelte components, reactivity, SvelteKit data loading, form
actions, or rendering boundaries. Repository authorities and the current
component contract determine the scope.

## Establish Version And Mode

Inspect `package.json`, the lockfile, Svelte configuration, and neighboring
components. Confirm the installed Svelte and SvelteKit versions and whether the
changed component uses legacy or runes mode. Check version-sensitive APIs against
primary docs before using them.

Svelte 5 supports legacy components alongside runes components. Extend the
current component's mode and preserve its props, events, slots or snippets, and
binding behavior. For new components, follow the repository's chosen mode. Treat
conversion to runes, callback props, or snippets as a migration when it changes
an existing contract; an unrelated bug fix does not authorize that conversion.

## Reactivity And Lifecycle

In runes components, use `$derived` for values computed from reactive inputs.
Use `$effect` for synchronization with an external system and release resources
when that synchronization ends. Effects run in the browser, so a value needed
for server rendering must not depend on an effect. Keep derived computation in
the repository's corresponding reactive mechanism for legacy components.

When extracting reactive state or reading props, check that the consumer retains
the needed reactive connection. Verify updates after a prop or route-data change,
not just the initial render: SvelteKit can reuse page and layout components
across navigation.

## Server And Client Boundaries

For server-rendered code, keep request-specific mutable state scoped to the
request or component tree. A mutable module singleton can share one user's data
with another. Follow the repository's request/context/state ownership rather
than introducing a global store for convenience.

SvelteKit universal `load` can execute on the server and in the browser. Keep
secrets, database access, and private imports in server-only modules and server
loads or actions. Return only client-safe data; a server-only file does not make
its returned data private. Keep browser-only APIs such as `window` and `document`
inside a suitable client lifecycle or the repository's explicit browser guard.

Preserve load serialization, error and redirect behavior, and form-action response
contracts. When a form uses progressive enhancement, verify its ordinary submit
and enhanced paths. Check server rendering and client navigation when the changed
boundary participates in both.

## Primary Sources

Consult only the mechanics reached by the change, checking version notes against
the installed packages:

- [Svelte 5 migration guide](https://svelte.dev/docs/svelte/v5-migration-guide) — legacy compatibility and migration boundaries.
- [Derived state](https://svelte.dev/docs/svelte/$derived) and [effects](https://svelte.dev/docs/svelte/$effect) — reactive computation and synchronization.
- [SvelteKit state management](https://svelte.dev/docs/kit/state-management) — request isolation and component reuse.
- [SvelteKit loading data](https://svelte.dev/docs/kit/load) — universal/server load and returned data.
- [Server-only modules](https://svelte.dev/docs/kit/server-only-modules) — private import boundaries.
- [Form actions](https://svelte.dev/docs/kit/form-actions) — submit and enhancement contracts.
