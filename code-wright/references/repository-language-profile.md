# Repository Profile

Use `.codewright.toml` at the repository root to share natural-language choices and Code Wright's shape-approval mode across contributors and agent harnesses. The profile belongs in version control; it is not a personal preference file.

The `$code-wright` skill keeps the `.codewright.toml` filename for compatibility with existing repository profiles.

## Discovery

Resolve the repository root from the active worktree and read exactly one `.codewright.toml` from that root. Do not search parent home directories or invent nested profiles.

If the file is absent during implementation, offer the first-use setup below once in the current conversation. If the user skips it or leaves it unanswered, continue with scoped repository authorities and the built-in defaults without creating files. In review-only work, report relevant missing settings without offering or writing setup. An existing profile does not prove every field is configured; use the fallback rules for omitted or invalid values without restarting onboarding.

## First-Use Setup

Read this schema and the applicable repository authorities before proposing settings. Use those authorities to settle existing policy; do not inspect unrelated projects to guess preferences.

Offer one compact setup question covering the unresolved choices:

- The language for code comments, code API documentation, and test descriptions. Let the user choose one language for all three or separate languages. Where no authority selects a language, explain that the built-in default is `en`; the conversation language alone does not select a shared repository policy.
- Shape approval: `ask` presents new placement and waits when it is not already approved; `auto` explains an in-scope placement and continues when ownership is settled. Recommend `ask` unless the user has requested fewer placement questions.
- Whether to record a language rule for README/general documentation and for agent-facing instructions in `AGENTS.md`. These are optional, separate from the three profile surfaces; keep existing rules and do not infer them from the code language.

For example, when no policy exists:

> Code Wright의 저장소 설정을 정할까요? 코드 주석·API 문서·테스트 설명은 각각 어떤 언어로 쓸까요(기본값: 영어, 세 항목을 한 언어로 지정 가능)? 새 코드 배치를 설명한 뒤 승인을 기다리는 `ask`와, 작업 범위와 소유자가 정해졌으면 계속하는 `auto` 중 선택해주세요(기본값: `ask`). README·일반 문서와 에이전트용 지침의 언어도 AGENTS.md에 기록하려면 함께 알려주세요. 설정을 건너뛰고 현재 작업을 계속해도 됩니다.

If the current request already specifies these choices and authorizes saving them, use it without another question. Accepting setup authorizes creating the root `.codewright.toml` with the resolved choices; changing an existing profile requires a request to save the new choices. Update existing keys in place and preserve unrelated settings. Resolve an unsupported or malformed existing profile under the fallback rules below before replacing it. Omit unanswered language keys and use their defaults; missing shape defaults to `ask`, never `auto`. Do not save a provisional default while awaiting an answer. A choice for this task alone does not authorize persistence.

If the user also chooses to save documentation language rules, update the applicable `AGENTS.md` section in place. Record the selected languages for README/general documentation and agent-facing instructions independently. Preserve unrelated content and avoid duplicate rules. Setup does not authorize translating existing documents. Before an authorized write, show the resolved values and intended files; do not ask again for a decision already made. Validate the saved TOML and its agreement with repository authorities, then report what future runs will read. Do not create a separate onboarding marker; a skipped offer is remembered only for this conversation.

## Version 1 Schema

```toml
version = 1

[language]
comments = "en"
api_documentation = "en"
test_descriptions = "en"

[approval]
shape = "ask"
```

Language values use BCP 47 language tags such as `ko`, `en`, or `ja`. A region may be included when it changes the writing policy, for example `pt-BR`.

- `comments` controls production and test code comments.
- `api_documentation` controls documentation attached to code APIs, such as rustdoc or docstrings.
- `test_descriptions` controls scenario and expected-result descriptions around tests.

The profile does not control identifiers, serialized field names, protocol vocabulary, commit messages, README/general documentation, agent-facing Markdown instructions, or the assistant's response language. Documentation language rules belong in repository authorities such as `AGENTS.md`.

Apply the three language settings independently. English instructions and examples do not override a configured language such as `ko`. When editing an existing file, apply the resolved setting to the changed prose; a scoped change does not by itself authorize translating the surrounding file.

## Shape Approval

`[approval]` is optional. Its `shape` value has two modes:

- `"ask"` (default): show a new file/module/test placement and wait for approval, unless the shape is already approved, including a consistent extension of an approved hierarchy without widening its surface.
- `"auto"`: show a brief placement and responsibility explanation, then continue without a separate approval question for an in-scope change with settled ownership.

This setting changes only the **Confirm shape** pause. It does not remove grounding, responsibility-boundary checks, verification, or review. New product, security, trust, or ownership decisions still require resolution. A user or repository instruction requiring approval takes precedence; execution permissions and authority for external actions are unchanged.

Use `"auto"` to avoid repeated placement questions; do not treat it as blanket approval to refactor unrelated code or change the profile itself. If `[approval]` or `shape` is missing, use `"ask"`. If the approval section or value is invalid, report it and use `"ask"`; do not infer auto approval from another key or a truthy value. Valid language settings remain usable when only the approval setting is invalid.

## Precedence And Drift

For each configured surface, apply the current user instruction first, then the nearest scoped repository authority, then `.codewright.toml`, then the built-in default.

When a scoped authority and the profile disagree, follow the scoped authority for the current change and report the stale pair. Do not silently rewrite either file. A one-off user request changes only the current task unless the user explicitly asks to update the shared profile.

Do not interpret an unknown `version` or malformed TOML. Report the profile as unsupported and fall back to scoped repository authorities and the built-in defaults, including `"ask"` for shape approval; ask before changing the file.
