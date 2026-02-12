# Svelte 5 API Reference

## $state

Reactive state declaration. Creates deeply reactive state by default.

```svelte
<script>
  let count = $state(0);
  let items = $state([1, 2, 3]); // array mutations (push, splice) are reactive
  let user = $state({ name: 'Kim', age: 30 }); // property changes are reactive
</script>
```

### $state.raw

Opts out of deep reactivity. Only reassignment triggers updates (not property mutations).

```svelte
<script>
  let data = $state.raw({ large: 'object' });
  // data.large = 'changed'; // will NOT trigger update
  data = { large: 'changed' }; // WILL trigger update
</script>
```

Use for large objects/arrays where you always replace rather than mutate, or for objects that should not be proxied (e.g., instances of third-party classes).

### $state.snapshot

Returns a plain (non-reactive, non-proxied) snapshot of `$state` value. Useful for passing to external libraries or `structuredClone`/`JSON.stringify`.

```ts
let items = $state([1, 2, 3]);
console.log($state.snapshot(items)); // plain array, not a proxy
```

### $state.eager

Forces immediate UI updates, bypassing Svelte's batched update system. Useful for user-facing feedback during async operations.

```svelte
<a href="/" aria-current={$state.eager(pathname) === '/' ? 'page' : null}>
```

### $state in classes

```ts
class Counter {
  count = $state(0);
  doubled = $derived(this.count * 2);

  increment() {
    this.count++;
  }
}
```

---

## $derived

Computed values that automatically track dependencies.

```svelte
<script>
  let count = $state(0);
  let doubled = $derived(count * 2);
  let message = $derived(`Count is ${count}`);
</script>
```

### $derived.by

For multi-statement computations:

```svelte
<script>
  let items = $state([3, 1, 4, 1, 5]);
  let sorted = $derived.by(() => {
    const copy = [...items];
    copy.sort((a, b) => a - b);
    return copy;
  });
</script>
```

### Dependency tracking

`$derived` automatically tracks any reactive values read synchronously during evaluation. Async operations or values read inside `setTimeout` etc. are NOT tracked.

### Overriding $derived (v5.25+)

A `$derived` value can be temporarily overridden by assignment. It reverts to the derived value when dependencies change.

```svelte
<script>
  let count = $state(0);
  let doubled = $derived(count * 2);
  // doubled = 99; // temporarily overrides; next time count changes, it recomputes
</script>
```

---

## $effect

Runs side effects when reactive dependencies change. Runs after the DOM has been updated.

```svelte
<script>
  let count = $state(0);

  $effect(() => {
    console.log(`count is ${count}`);

    // optional cleanup function
    return () => {
      console.log('cleaning up');
    };
  });
</script>
```

### Cleanup

Return a function from `$effect` to run cleanup before re-execution or when the component is destroyed.

```svelte
<script>
  let width = $state(window.innerWidth);

  $effect(() => {
    const handler = () => (width = window.innerWidth);
    window.addEventListener('resize', handler);
    return () => window.removeEventListener('resize', handler);
  });
</script>
```

### $effect.pre

Runs before DOM updates. Same as `$effect` but with pre-update timing.

```svelte
<script>
  $effect.pre(() => {
    // runs before DOM is updated
  });
</script>
```

### $effect.tracking

Returns `true` if called inside a tracking context ($derived or $effect).

```ts
$effect(() => {
  console.log($effect.tracking()); // true
});
console.log($effect.tracking()); // false
```

### $effect.root

Creates a non-tracked root scope for effects. Must be manually cleaned up. Useful outside component context.

```ts
const cleanup = $effect.root(() => {
  $effect(() => {
    // this effect is not tied to a component lifecycle
  });
});
// later: cleanup();
```

### When NOT to use $effect

- **Do NOT use to sync state**: Use `$derived` instead.
  ```svelte
  <!-- BAD -->
  <script>
    let count = $state(0);
    let doubled = $state(0);
    $effect(() => { doubled = count * 2; }); // WRONG
  </script>

  <!-- GOOD -->
  <script>
    let count = $state(0);
    let doubled = $derived(count * 2); // CORRECT
  </script>
  ```
- **Do NOT use for event-driven state updates**: Handle in event handlers instead.

---

## $props

Declares component props. Must be called at the top level of `<script>`.

```svelte
<script>
  let { name, age = 25 } = $props();
</script>
```

### Default values

```svelte
<script>
  let { variant = 'primary', size = 'md' } = $props();
</script>
```

### Renaming

```svelte
<script>
  let { class: className = '' } = $props();
</script>
```

### Rest props

```svelte
<script>
  let { title, ...rest } = $props();
</script>
<div {...rest}>{title}</div>
```

### $props.id() (v5.20+)

Generates a unique, deterministic ID. Useful for associating labels with form elements.

```svelte
<script>
  let { label } = $props();
  const id = $props.id();
</script>
<label for={id}>{label}</label>
<input {id} />
```

### TypeScript

```svelte
<script lang="ts">
  interface Props {
    name: string;
    age?: number;
    onchange?: (value: string) => void;
  }
  let { name, age = 25, onchange }: Props = $props();
</script>
```

---

## $bindable

Declares a prop as bindable (two-way binding).

```svelte
<!-- TextInput.svelte -->
<script lang="ts">
  let { value = $bindable('') }: { value: string } = $props();
</script>
<input bind:value oninput={() => {}} />

<!-- Parent.svelte -->
<script>
  import TextInput from './TextInput.svelte';
  let text = $state('');
</script>
<TextInput bind:value={text} />
```

The default value passed to `$bindable()` is used when the parent does NOT use `bind:`.

---

## $inspect

Development-only reactive debugging. Automatically stripped in production builds.

```svelte
<script>
  let count = $state(0);
  $inspect(count); // logs to console whenever count changes
  $inspect(count, 'label'); // with label
</script>
```

### $inspect(...).with(fn)

Custom callback instead of `console.log`:

```svelte
<script>
  let count = $state(0);
  $inspect(count).with((type, ...values) => {
    // type: 'init' | 'update'
    if (type === 'update') debugger;
  });
</script>
```

### $inspect.trace() (v5.14+)

Traces which reactive values caused the current `$effect` or `$derived` to re-run.

```svelte
<script>
  $effect(() => {
    $inspect.trace();
    // ... when this effect re-runs, the console will show which values changed
  });
</script>
```

---

## Snippets

Reusable markup blocks defined inside a component. Replace slots from Svelte 4.

### Basic snippet

```svelte
{#snippet greeting(name)}
  <p>Hello, {name}!</p>
{/snippet}

{@render greeting('World')}
{@render greeting('Svelte')}
```

### Snippets with no parameters

```svelte
{#snippet header()}
  <h1>Title</h1>
{/snippet}

{@render header()}
```

### Optional rendering

```svelte
{#if footer}
  {@render footer()}
{/if}
```

### Passing snippets to components

Snippets can be passed as props to child components:

```svelte
<!-- Parent -->
<Card>
  {#snippet header()}
    <h2>Title</h2>
  {/snippet}
  {#snippet body()}
    <p>Content here</p>
  {/snippet}
</Card>

<!-- Card.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';
  let { header, body }: { header: Snippet; body: Snippet } = $props();
</script>
<div class="card">
  <div class="header">{@render header()}</div>
  <div class="body">{@render body()}</div>
</div>
```

### children snippet

Content placed directly between component tags becomes the `children` snippet:

```svelte
<!-- Parent -->
<Card>
  <p>This becomes the children snippet</p>
</Card>

<!-- Card.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';
  let { children }: { children: Snippet } = $props();
</script>
<div class="card">
  {@render children()}
</div>
```

### Snippet types

```ts
import type { Snippet } from 'svelte';

interface Props {
  header: Snippet;
  row: Snippet<[item: Item]>;
  children: Snippet;
}
```

---

## Event Handling

Svelte 5 uses native DOM event attributes directly. No more `on:` directive.

### Native events

```svelte
<button onclick={() => count++}>Click</button>
<input oninput={(e) => value = e.currentTarget.value} />
<form onsubmit={(e) => { e.preventDefault(); handleSubmit(e); }}>
```

**Event modifiers are removed** in Svelte 5. No `|preventDefault`, `|stopPropagation`, `|once` etc. Handle inline:

```svelte
<form onsubmit={(e) => { e.preventDefault(); handleSubmit(e); }}>
```

For `capture` events, use the naming convention `onclickcapture`:

```svelte
<div onclickcapture={(e) => console.log('capture phase')}>
```

### Component events (callback props)

```svelte
<!-- Child.svelte -->
<script lang="ts">
  let { onclick }: { onclick: (detail: string) => void } = $props();
</script>
<button onclick={() => onclick('clicked!')}>Click me</button>

<!-- Parent.svelte -->
<Child onclick={(msg) => console.log(msg)} />
```

### Event forwarding

No special syntax needed — just spread rest props:

```svelte
<script>
  let { children, ...rest } = $props();
</script>
<button {...rest}>{@render children()}</button>
```

---

## Component API

### mount

Imperatively mount a component to a DOM target.

```ts
import { mount } from 'svelte';
import App from './App.svelte';

const app = mount(App, {
  target: document.getElementById('app')!,
  props: { name: 'World' }
});
```

### unmount

```ts
import { unmount } from 'svelte';
unmount(app);
```

### hydrate

For SSR hydration:

```ts
import { hydrate } from 'svelte';
import App from './App.svelte';

const app = hydrate(App, {
  target: document.getElementById('app')!,
  props: { name: 'World' }
});
```

### untrack

Reads reactive values without creating a dependency:

```ts
import { untrack } from 'svelte';

$effect(() => {
  // `count` is tracked, `other` is NOT tracked
  console.log(count, untrack(() => other));
});
```

### Other svelte module utilities

```ts
import {
  tick,
  flushSync,
  settled,
  fork,
  createRawSnippet,
  createContext,
  getContext,
  setContext,
  getAllContexts,
  hasContext,
  onMount,
  onDestroy,
  getAbortSignal,
} from 'svelte';
```

| Function | Description |
|----------|-------------|
| `tick()` | Returns a promise that resolves after pending state changes apply to DOM |
| `flushSync(fn?)` | Synchronously applies pending updates |
| `settled()` | Resolves after state changes AND resulting async work complete |
| `fork(fn)` | Creates off-screen evaluation space; returns `{ commit(), discard() }` |
| `createRawSnippet(fn)` | Programmatic snippet creation |
| `createContext()` | Returns `[get, set]` pair for type-safe context |
| `getAbortSignal()` | Returns AbortSignal that aborts when containing effect/derived re-runs |
| `onMount(fn)` | Runs after component mounts (not during SSR) |
| `onDestroy(fn)` | Runs before component unmounts |

---

## $host

Available only in custom element components (`<svelte:options customElement="...">`). Returns the host DOM element.

```svelte
<svelte:options customElement="my-stepper" />

<script>
  function dispatch(type) {
    $host().dispatchEvent(new CustomEvent(type));
  }
</script>

<button onclick={() => dispatch('decrement')}>-</button>
<button onclick={() => dispatch('increment')}>+</button>
```
