# SvelteKit API Reference

## Routing

SvelteKit uses file-based routing in `src/routes/`.

### File conventions

| File | Purpose |
|------|---------|
| `+page.svelte` | Page component (UI) |
| `+page.ts` | Universal load function (runs on server + client) |
| `+page.server.ts` | Server-only load function + form actions |
| `+layout.svelte` | Layout component (wraps child pages) |
| `+layout.ts` | Universal layout load function |
| `+layout.server.ts` | Server-only layout load function |
| `+error.svelte` | Error boundary page |
| `+server.ts` | API endpoint (GET, POST, PUT, DELETE, etc.) |

### Dynamic parameters

```
src/routes/blog/[slug]/+page.svelte    → /blog/hello-world
src/routes/[category]/[id]/+page.svelte → /news/123
```

### Rest parameters

```
src/routes/files/[...path]/+page.svelte → /files/a/b/c  (params.path = 'a/b/c')
```

### Optional parameters

```
src/routes/[[lang]]/about/+page.svelte → /about OR /ko/about
```

### Route groups

Parenthesized directories group routes without affecting the URL:

```
src/routes/(auth)/login/+page.svelte   → /login
src/routes/(auth)/signup/+page.svelte  → /signup
src/routes/(app)/dashboard/+page.svelte → /dashboard
```

Each group can have its own `+layout.svelte`.

### Layout reset

Use `@` to reset to a parent layout:

```
src/routes/(app)/settings/+page@.svelte  → uses root layout instead of (app) layout
```

---

## Load Functions

### Universal load (`+page.ts` / `+layout.ts`)

Runs on both server and client. Cannot access DB, filesystem, or private env vars.

```ts
// src/routes/blog/[slug]/+page.ts
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch, url, depends }) => {
  const res = await fetch(`/api/posts/${params.slug}`);
  const post = await res.json();

  depends('app:post'); // custom invalidation key

  return { post };
};
```

### Server load (`+page.server.ts` / `+layout.server.ts`)

Runs only on the server. Can access DB, secrets, private env vars.

```ts
// src/routes/blog/[slug]/+page.server.ts
import type { PageServerLoad } from './$types';
import { db } from '$lib/server/db';

export const load: PageServerLoad = async ({ params }) => {
  const post = await db.posts.findUnique({ where: { slug: params.slug } });
  if (!post) throw error(404, 'Not found');
  return { post };
};
```

### Load function input

Common parameters available in load functions:

| Parameter | Description |
|-----------|-------------|
| `params` | Route parameters |
| `url` | Current URL object |
| `route` | Route info (`{ id: '/blog/[slug]' }`) |
| `fetch` | Enhanced fetch (relative URLs, cookie forwarding) |
| `depends` | Register custom dependency for invalidation |
| `parent` | Get data from parent layout's load function |
| `untrack` | Read values without dependency tracking |

Server-only additional parameters:

| Parameter | Description |
|-----------|-------------|
| `cookies` | Read/set cookies |
| `locals` | Per-request data set in hooks |
| `request` | Original Request object |
| `platform` | Platform-specific data |

### await parent()

Access parent layout data:

```ts
export const load: PageServerLoad = async ({ parent }) => {
  const { user } = await parent();
  // use user data from layout load
};
```

### Invalidation

```ts
import { invalidate, invalidateAll } from '$app/navigation';

// Invalidate specific dependency
invalidate('app:post');
invalidate('/api/posts');

// Invalidate everything
invalidateAll();
```

---

## Form Actions

Defined in `+page.server.ts`. Handle form submissions server-side.

### Default action

```ts
// src/routes/login/+page.server.ts
import type { Actions } from './$types';
import { fail, redirect } from '@sveltejs/kit';

export const actions: Actions = {
  default: async ({ request, cookies }) => {
    const data = await request.formData();
    const email = data.get('email') as string;
    const password = data.get('password') as string;

    const user = await authenticate(email, password);
    if (!user) {
      return fail(400, { email, message: 'Invalid credentials' });
    }

    cookies.set('session', user.token, { path: '/' });
    redirect(303, '/dashboard');
  }
};
```

### Named actions

```ts
export const actions: Actions = {
  login: async ({ request }) => { /* ... */ },
  register: async ({ request }) => { /* ... */ },
};
```

Use in form:

```svelte
<form method="POST" action="?/login">...</form>
<form method="POST" action="?/register">...</form>
```

### fail()

Return validation errors without redirect:

```ts
return fail(400, {
  email,
  errors: { email: 'Invalid email format' }
});
```

### use:enhance

Progressive enhancement for forms. Prevents full page reload.

```svelte
<script>
  import { enhance } from '$app/forms';
</script>

<form method="POST" use:enhance>
  <!-- form fields -->
</form>
```

Custom enhance callback:

```svelte
<form method="POST" use:enhance={({ formData, cancel }) => {
  // runs before submission
  if (!confirm('Are you sure?')) cancel();

  return async ({ result, update }) => {
    // runs after submission
    if (result.type === 'success') {
      // handle success
    }
    await update(); // apply default behavior (update form prop)
  };
}}>
```

### Accessing action data in page

```svelte
<!-- +page.svelte -->
<script>
  let { form } = $props();
  // form contains the return value from the action (including fail() data)
</script>

{#if form?.message}
  <p class="error">{form.message}</p>
{/if}
```

---

## Hooks

Defined in `src/hooks.server.ts` (server) and `src/hooks.client.ts` (client).

### handle (server)

Intercepts every request. Can modify request/response.

```ts
// src/hooks.server.ts
import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  // Before route handling
  const session = event.cookies.get('session');
  if (session) {
    event.locals.user = await getUserFromSession(session);
  }

  // Resolve the request
  const response = await resolve(event, {
    transformPageChunk: ({ html }) => html.replace('%lang%', 'ko')
  });

  return response;
};
```

Sequence multiple handlers:

```ts
import { sequence } from '@sveltejs/kit/hooks';

export const handle = sequence(authHandle, loggingHandle);
```

### handleFetch (server)

Customize fetch behavior for server-side requests made during load.

```ts
export const handleFetch: HandleFetch = async ({ request, fetch, event }) => {
  if (request.url.startsWith('https://api.internal/')) {
    request = new Request(
      request.url.replace('https://api.internal/', 'http://localhost:3000/'),
      request
    );
  }
  return fetch(request);
};
```

### handleError (server & client)

Handle unexpected errors. Return a user-safe error object.

```ts
// src/hooks.server.ts
export const handleError: HandleServerError = async ({ error, event, status, message }) => {
  const errorId = crypto.randomUUID();
  console.error(error, errorId);
  return {
    message: 'An unexpected error occurred',
    errorId
  };
};
```

```ts
// src/hooks.client.ts
export const handleError: HandleClientError = async ({ error, status, message }) => {
  return {
    message: 'Something went wrong',
  };
};
```

### handleValidationError (server)

Called when remote function arguments fail schema validation. Be cautious — validation failures may indicate malicious requests.

```ts
export const handleValidationError: HandleValidationError = ({ issues, event }) => {
  return { message: 'Validation failed' }; // must match App.Error shape
};
```

### init (server)

Runs once when the server starts. Use for one-time initialization.

```ts
export const init: ServerInit = async () => {
  await db.connect();
};
```

### reroute

Rewrite URLs before routing. Defined in `src/hooks.ts` (shared). Can be async since SvelteKit 2.18.

```ts
// src/hooks.ts
import type { Reroute } from '@sveltejs/kit';

export const reroute: Reroute = ({ url }) => {
  if (url.pathname === '/old-path') {
    return '/new-path';
  }
};
```

### transport

Define custom serialization for data passed from server to client. Defined in `src/hooks.ts`.

```ts
// src/hooks.ts
import type { Transport } from '@sveltejs/kit';

export const transport: Transport = {
  Date: {
    encode: (value) => value instanceof Date && value.toISOString(),
    decode: (value) => new Date(value)
  }
};
```

---

## Page Options

Export from `+page.ts`, `+page.server.ts`, `+layout.ts`, or `+layout.server.ts`.

```ts
export const ssr = true;        // enable/disable server-side rendering
export const csr = true;        // enable/disable client-side rendering
export const prerender = false; // enable/disable prerendering
export const trailingSlash = 'never'; // 'never' | 'always' | 'ignore'
```

Layout-level options apply to all child pages.

---

## API Routes (+server.ts)

```ts
// src/routes/api/posts/+server.ts
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
  const limit = Number(url.searchParams.get('limit') ?? 10);
  const posts = await db.posts.findMany({ take: limit });
  return json(posts);
};

export const POST: RequestHandler = async ({ request }) => {
  const body = await request.json();
  const post = await db.posts.create({ data: body });
  return json(post, { status: 201 });
};

export const DELETE: RequestHandler = async ({ params }) => {
  await db.posts.delete({ where: { id: params.id } });
  return new Response(null, { status: 204 });
};
```

---

## Modules

### $app/state

Reactive page state (replaces deprecated `$app/stores`).

```svelte
<script>
  import { page, navigating, updated } from '$app/state';
</script>

<!-- Access current page data -->
<p>URL: {page.url.pathname}</p>
<p>Params: {page.params.slug}</p>
<p>Data: {page.data.title}</p>
<p>Form: {page.form?.message}</p>
<p>Status: {page.status}</p>
<p>Error: {page.error?.message}</p>

<!-- Check navigation status -->
{#if navigating.to}
  <p>Navigating to {navigating.to.url.pathname}...</p>
{/if}

<!-- Check for app updates -->
{#if updated.current}
  <p>New version available! <button onclick={() => location.reload()}>Reload</button></p>
{/if}
```

### $app/navigation

```ts
import {
  goto,
  invalidate,
  invalidateAll,
  preloadData,
  preloadCode,
  beforeNavigate,
  afterNavigate,
  onNavigate,
  pushState,
  replaceState
} from '$app/navigation';

// Navigate programmatically
goto('/dashboard');
goto('/login', { replaceState: true });

// Invalidation
invalidate('app:data');
invalidateAll();

// Lifecycle navigation hooks
beforeNavigate(({ cancel, to, from, willUnload }) => {
  if (hasUnsavedChanges && !confirm('Discard changes?')) cancel();
});

afterNavigate(({ from, to, type }) => {
  // runs after navigation completes
});

onNavigate(({ from, to }) => {
  // runs during navigation, can return a promise for view transitions
});

// Shallow routing (client-side state in history)
pushState('/modal', { showModal: true });
replaceState('', { showModal: false });
```

### $app/forms

```ts
import { enhance, applyAction, deserialize } from '$app/forms';
```

### $app/server

```ts
import { read } from '$app/server';
// Read assets imported with ?url in server context
```

### $env

```ts
import { PUBLIC_API_URL } from '$env/static/public';   // available on client + server
import { SECRET_KEY } from '$env/static/private';        // server only
import { env } from '$env/dynamic/public';               // runtime, client + server
import { env } from '$env/dynamic/private';              // runtime, server only
```

---

## Server-only Module Rules

The following are restricted to server-side code only. Importing them from client code causes a build error:

1. **`.server.ts` / `.server.js` suffix**: Any file named `*.server.ts` cannot be imported from client code.
2. **`$lib/server/` directory**: Everything inside `src/lib/server/` is server-only.
3. **`$env/static/private`** and **`$env/dynamic/private`**: Private environment variables.
4. **`+page.server.ts` / `+layout.server.ts`**: Their load functions and actions only run on the server.

This is enforced at build time to prevent accidentally leaking secrets to the client bundle.
