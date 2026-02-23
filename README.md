[한국어](README.ko.md)

# Claude Code Agents

A collection of reusable sub-agents (skills) for Claude Code that can be used globally across all projects.

Each agent is managed as an independent directory and can be made available in any project by creating symlinks under `~/.claude/skills/`.

## Installation

```bash
git clone <repo-url> ~/project/claude-code-agents
cd ~/project/claude-code-agents
./install.sh install
```

Restart Claude Code and the agents will be automatically recognized.

## Uninstall

```bash
cd ~/project/claude-code-agents
./install.sh uninstall
```

## Available Agents

| Agent | Command | Description |
|-------|---------|-------------|
| Svelte 5 | `/svelte5` | Svelte 5 runes syntax, SvelteKit patterns, component generation, code review, debugging |
| Rust Axum Backend | `/rust-axum-backend` | Axum 0.8.x API routing, handler/extractor patterns, serde serialization, request validation, utoipa OpenAPI docs, error handling, project structure |
| Rust Style | `/rust-style` | Framework-agnostic Rust style conventions — use sorting, module structure, naming, error design, documentation, idiomatic patterns |

## Adding a New Agent

1. Create a new directory (e.g., `react/`)
2. Write a `SKILL.md` file (frontmatter + prompt)
3. Add any reference files needed
4. Re-run `./install.sh install`

## Usage Examples

```
/svelte5 Create a Counter component
/svelte5 Review this code
/svelte5 Show me how to use $effect

/rust-axum-backend Create CRUD API handlers
/rust-axum-backend Set up the project structure
/rust-axum-backend Add OpenAPI documentation

/rust-style Review this file's style
/rust-style Organize imports in src/
/rust-style Set up rustfmt and Clippy config
```
