# Official guidance

Use this source map for instruction selection and host compatibility questions.
The skill's selection rules are a synthesis; host mechanics remain defined by
the target tool's current documentation and configuration. Read only the
relevant source when a claim needs checking, not all sources on every edit.

## Format and writing

- [AGENTS.md](https://agents.md/): plain Markdown, with no required headings or
  fields. Its examples are optional content, not a mandatory development template.
- [OpenAI: Rethinking skills and prompts](https://learn.chatgpt.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra):
  use narrow triggers and conditional references; remove scaffolding made
  redundant by model improvements. Different models may need different amounts
  of support, so keep detailed help off the default path.
- [Anthropic: Claude Code best practices](https://code.claude.com/docs/en/best-practices#keep-claude-md-short):
  prioritize project facts and conventions the agent cannot cheaply discover;
  move task procedures to skills. Generic persistence prompts and added emphasis
  can cause unnecessary work. These recommendations do not invalidate explicit
  project requirements.

## Loading and scope

Consult these sources before relying on tool-specific discovery or changing
instruction wiring. Inspect the target runtime and configuration; describe
untested compatibility as unverified. A Markdown link is not a portable import
mechanism.

- [OpenAI: Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md):
  Codex builds a launch-time chain from global guidance and the project-root to
  working-directory path. Overrides, fallback names, and the configured size
  limit affect what is included. A nested file's existence does not prove it
  applies to the current launch directory.
- [Anthropic: Project memory](https://code.claude.com/docs/en/memory#agentsmd):
  Claude Code's AGENTS.md support depends on version, settings, and other
  instruction files. Confirm which files actually load before adding an import
  or compatibility file; an extra wrapper may be unnecessary. Its discovery and
  import rules differ from Codex's.

Instruction text guides behavior; enforcement belongs to tool or project
controls. Keep compatibility changes within the requested scope.

## Local authoring choices

Concise English is this skill's default, not an AGENTS.md format requirement.
The optional drafting guide is support for a demonstrated need or explicit
request, not a fixed model tier. Use no universal line limit or model-name
threshold. Preserve policy when pruning repetition, and validate claimed
benefits with representative tasks rather than assuming more text helps.
