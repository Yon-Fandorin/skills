# Svelte 5 / SvelteKit Examples

## 1. Basic Counter (Runes)

```svelte
<!-- Counter.svelte -->
<script lang="ts">
  let count = $state(0);
  let doubled = $derived(count * 2);

  function increment() {
    count++;
  }

  function reset() {
    count = 0;
  }
</script>

<div>
  <p>Count: {count}</p>
  <p>Doubled: {doubled}</p>
  <button onclick={increment}>+1</button>
  <button onclick={reset}>Reset</button>
</div>
```

---

## 2. Form Component ($props + $bindable)

```svelte
<!-- TextInput.svelte -->
<script lang="ts">
  interface Props {
    label: string;
    value: string;
    error?: string;
    type?: 'text' | 'email' | 'password';
  }

  let { label, value = $bindable(''), error, type = 'text' }: Props = $props();
  const id = $props.id();
</script>

<div class="field">
  <label for={id}>{label}</label>
  <input {id} {type} bind:value class:error={!!error} />
  {#if error}
    <p class="error-message">{error}</p>
  {/if}
</div>

<style>
  .error { border-color: red; }
  .error-message { color: red; font-size: 0.875rem; }
</style>
```

```svelte
<!-- LoginForm.svelte -->
<script lang="ts">
  import TextInput from './TextInput.svelte';

  let email = $state('');
  let password = $state('');
  let errors = $state<Record<string, string>>({});

  function validate() {
    const newErrors: Record<string, string> = {};
    if (!email.includes('@')) newErrors.email = 'Invalid email';
    if (password.length < 8) newErrors.password = 'Minimum 8 characters';
    errors = newErrors;
    return Object.keys(newErrors).length === 0;
  }

  function handleSubmit(e: SubmitEvent) {
    e.preventDefault();
    if (validate()) {
      console.log('Submit:', { email, password });
    }
  }
</script>

<form onsubmit={handleSubmit}>
  <TextInput label="Email" bind:value={email} error={errors.email} type="email" />
  <TextInput label="Password" bind:value={password} error={errors.password} type="password" />
  <button type="submit">Login</button>
</form>
```

---

## 3. List with Snippets

```svelte
<!-- UserList.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface User {
    id: number;
    name: string;
    role: string;
  }

  interface Props {
    users: User[];
    header?: Snippet;
    row: Snippet<[User]>;
    empty?: Snippet;
  }

  let { users, header, row, empty }: Props = $props();
</script>

{#if header}
  {@render header()}
{/if}

{#if users.length === 0}
  {#if empty}
    {@render empty()}
  {:else}
    <p>No users found.</p>
  {/if}
{:else}
  <ul>
    {#each users as user (user.id)}
      <li>{@render row(user)}</li>
    {/each}
  </ul>
{/if}
```

```svelte
<!-- Usage -->
<script>
  import UserList from './UserList.svelte';

  let users = $state([
    { id: 1, name: 'Alice', role: 'Admin' },
    { id: 2, name: 'Bob', role: 'User' },
  ]);
</script>

<UserList {users}>
  {#snippet header()}
    <h2>Team Members</h2>
  {/snippet}

  {#snippet row(user)}
    <span>{user.name} ({user.role})</span>
  {/snippet}

  {#snippet empty()}
    <p>No team members yet.</p>
  {/snippet}
</UserList>
```

---

## 4. $effect: External Library Integration

```svelte
<!-- Chart.svelte -->
<script lang="ts">
  import { Chart } from 'chart.js/auto';

  interface Props {
    data: number[];
    labels: string[];
  }

  let { data, labels }: Props = $props();
  let canvas: HTMLCanvasElement;

  $effect(() => {
    const chart = new Chart(canvas, {
      type: 'bar',
      data: {
        labels,
        datasets: [{ label: 'Values', data }],
      },
    });

    return () => {
      chart.destroy();
    };
  });
</script>

<canvas bind:this={canvas}></canvas>
```

---

## 5. $derived: Filter and Sort

```svelte
<!-- FilterableList.svelte -->
<script lang="ts">
  interface Item {
    id: number;
    name: string;
    category: string;
    price: number;
  }

  let { items }: { items: Item[] } = $props();

  let search = $state('');
  let sortBy = $state<'name' | 'price'>('name');
  let selectedCategory = $state<string>('all');

  let categories = $derived(['all', ...new Set(items.map((i) => i.category))]);

  let filtered = $derived.by(() => {
    let result = items;

    if (selectedCategory !== 'all') {
      result = result.filter((i) => i.category === selectedCategory);
    }

    if (search) {
      const q = search.toLowerCase();
      result = result.filter((i) => i.name.toLowerCase().includes(q));
    }

    result = [...result].sort((a, b) => {
      if (sortBy === 'price') return a.price - b.price;
      return a.name.localeCompare(b.name);
    });

    return result;
  });
</script>

<div>
  <input placeholder="Search..." bind:value={search} />

  <select bind:value={selectedCategory}>
    {#each categories as cat}
      <option value={cat}>{cat}</option>
    {/each}
  </select>

  <select bind:value={sortBy}>
    <option value="name">Name</option>
    <option value="price">Price</option>
  </select>

  <ul>
    {#each filtered as item (item.id)}
      <li>{item.name} - {item.category} - ${item.price}</li>
    {/each}
  </ul>

  <p>{filtered.length} items</p>
</div>
```

---

## 6. SvelteKit Route + Load Function

```
src/routes/blog/
├── +page.svelte          # Blog list page
├── +page.server.ts       # Load blog posts
└── [slug]/
    ├── +page.svelte      # Blog post page
    └── +page.server.ts   # Load single post
```

```ts
// src/routes/blog/+page.server.ts
import type { PageServerLoad } from './$types';
import { db } from '$lib/server/db';

export const load: PageServerLoad = async ({ url }) => {
  const page = Number(url.searchParams.get('page') ?? 1);
  const posts = await db.posts.findMany({
    take: 10,
    skip: (page - 1) * 10,
    orderBy: { createdAt: 'desc' },
  });
  const total = await db.posts.count();

  return { posts, page, totalPages: Math.ceil(total / 10) };
};
```

```svelte
<!-- src/routes/blog/+page.svelte -->
<script lang="ts">
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();
</script>

<h1>Blog</h1>

{#each data.posts as post}
  <article>
    <a href="/blog/{post.slug}">
      <h2>{post.title}</h2>
      <p>{post.excerpt}</p>
    </a>
  </article>
{/each}

<nav>
  {#if data.page > 1}
    <a href="?page={data.page - 1}">Previous</a>
  {/if}
  <span>Page {data.page} / {data.totalPages}</span>
  {#if data.page < data.totalPages}
    <a href="?page={data.page + 1}">Next</a>
  {/if}
</nav>
```

```ts
// src/routes/blog/[slug]/+page.server.ts
import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';
import { db } from '$lib/server/db';

export const load: PageServerLoad = async ({ params }) => {
  const post = await db.posts.findUnique({ where: { slug: params.slug } });
  if (!post) error(404, 'Post not found');
  return { post };
};
```

```svelte
<!-- src/routes/blog/[slug]/+page.svelte -->
<script lang="ts">
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();
</script>

<article>
  <h1>{data.post.title}</h1>
  <div>{@html data.post.content}</div>
</article>

<a href="/blog">Back to blog</a>
```

---

## 7. Form Actions + use:enhance

```ts
// src/routes/todos/+page.server.ts
import type { Actions, PageServerLoad } from './$types';
import { fail } from '@sveltejs/kit';
import { db } from '$lib/server/db';

export const load: PageServerLoad = async ({ locals }) => {
  const todos = await db.todos.findMany({
    where: { userId: locals.user.id },
    orderBy: { createdAt: 'desc' },
  });
  return { todos };
};

export const actions: Actions = {
  create: async ({ request, locals }) => {
    const data = await request.formData();
    const text = data.get('text') as string;

    if (!text?.trim()) {
      return fail(400, { text, error: 'Todo text is required' });
    }

    await db.todos.create({
      data: { text: text.trim(), userId: locals.user.id },
    });
  },

  toggle: async ({ request }) => {
    const data = await request.formData();
    const id = data.get('id') as string;
    const todo = await db.todos.findUnique({ where: { id } });
    if (todo) {
      await db.todos.update({
        where: { id },
        data: { completed: !todo.completed },
      });
    }
  },

  delete: async ({ request }) => {
    const data = await request.formData();
    const id = data.get('id') as string;
    await db.todos.delete({ where: { id } });
  },
};
```

```svelte
<!-- src/routes/todos/+page.svelte -->
<script lang="ts">
  import type { PageData, ActionData } from './$types';
  import { enhance } from '$app/forms';

  let { data, form }: { data: PageData; form: ActionData } = $props();
</script>

<h1>Todos</h1>

<form method="POST" action="?/create" use:enhance>
  <input name="text" value={form?.text ?? ''} placeholder="New todo..." />
  <button type="submit">Add</button>
  {#if form?.error}
    <p class="error">{form.error}</p>
  {/if}
</form>

<ul>
  {#each data.todos as todo (todo.id)}
    <li>
      <form method="POST" action="?/toggle" use:enhance>
        <input type="hidden" name="id" value={todo.id} />
        <button type="submit" class:completed={todo.completed}>
          {todo.text}
        </button>
      </form>

      <form method="POST" action="?/delete" use:enhance>
        <input type="hidden" name="id" value={todo.id} />
        <button type="submit" aria-label="Delete">x</button>
      </form>
    </li>
  {/each}
</ul>

<style>
  .completed { text-decoration: line-through; opacity: 0.6; }
</style>
```

---

## 8. API Endpoint (+server.ts)

```ts
// src/routes/api/users/+server.ts
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { db } from '$lib/server/db';

export const GET: RequestHandler = async ({ url }) => {
  const search = url.searchParams.get('q');
  const users = await db.users.findMany({
    where: search
      ? { name: { contains: search, mode: 'insensitive' } }
      : undefined,
    select: { id: true, name: true, email: true },
  });
  return json(users);
};

export const POST: RequestHandler = async ({ request }) => {
  const body = await request.json();

  if (!body.name || !body.email) {
    error(400, 'Name and email are required');
  }

  const user = await db.users.create({
    data: { name: body.name, email: body.email },
  });

  return json(user, { status: 201 });
};
```

```ts
// src/routes/api/users/[id]/+server.ts
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { db } from '$lib/server/db';

export const GET: RequestHandler = async ({ params }) => {
  const user = await db.users.findUnique({ where: { id: params.id } });
  if (!user) error(404, 'User not found');
  return json(user);
};

export const PATCH: RequestHandler = async ({ params, request }) => {
  const body = await request.json();
  const user = await db.users.update({
    where: { id: params.id },
    data: body,
  });
  return json(user);
};

export const DELETE: RequestHandler = async ({ params }) => {
  await db.users.delete({ where: { id: params.id } });
  return new Response(null, { status: 204 });
};
```
