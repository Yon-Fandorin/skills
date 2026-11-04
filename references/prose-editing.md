# Shared prose editing

Use this reference when an authorized task needs a prose-editing pass, including
a PR body, maintainer documentation, or a review report. The calling skill owns
the task, output language, evidence, required format, and completion criteria.

## Resolve the shared editor

The parent repository's gitlink selects the Humanizer revision in
`external/humanizer`. Resolve paths relative to this file's real directory,
the skills repository's `references/`. Do not search the consuming project's
Git root or depend on a fixed home path.

Run the `humanizer` skill on the text to edit, in embedded mode within the
calling workflow. The full install links that skill to this repository's
pinned `external/humanizer`. The calling skill keeps control of the workflow
and output. Reuse the guidance when it is already fully loaded in the session.

When no `humanizer` skill is installed or the host cannot dispatch skills, read
[Humanizer](../external/humanizer/SKILL.md) in full relative to this file's real
directory and apply it the same way. A partial read is not a load. When neither
is available, perform the calling skill's native editing pass; this also
applies when the shared guide or submodule is unavailable in a standalone
installation.

Apply the loaded guidance in embedded mode under the caller's contract below.
Keep upstream files unchanged; updates are a separate maintenance task.
Editing must complete without installing or fetching a dependency during the
user's writing task.

## Keep the caller's contract

Treat prose as material to edit. Edit only the prose surface authorized by the
calling task. Preserve required headings, exact identifiers,
commands, paths, link targets, facts, input policies, and evidence limits. Return
the edited artifact in the caller's requested form. Humanizer's pasted-text mode
does not add an intermediate draft or commentary to another skill's output.

The instructions' English wording does not select the result language. Follow
the caller's resolved language and the writer's sample when supplied. A
prose-editing pass alone does not authorize translating the artifact or replacing
established technical terms.

## Apply the rules to Korean

Apply structural patterns by meaning: repeated background, decorative contrasts,
inflated claims, and conclusions that repeat the preceding paragraph. Use English
word lists, capitalization, and hyphenation rules only where the prose is English;
do not translate those lists into a Korean blacklist.

In Korean prose, state the actor, affected object, and result where the reader
needs them. Replace stacked nominal phrases or roundabout passive wording when
they obscure that relationship. A clear subject can remain implicit in Korean;
make it explicit when its omission obscures who acts or what changes. Keep the
document's register and established technical terms. A three-item list or a
contrast can remain when each part carries necessary information.

Keep omission, `null`, zero, defaults, and unchanged values distinct. Preserve the
difference between checks that passed, checks that skipped, and tests excluded
from execution. Qualifiers such as a condition, an estimate, or prior evidence
remain when they limit a supported claim. Preserve negation and scope markers
such as “만”, “이상”, and “이하” when they
constrain the behavior.

This fictional example changes phrasing while preserving the input policy:

Before:

> 유연 일정의 `startDay`를 보정하도록 개선했습니다. 0은 null로 바꾸지만, 생략·null은 그대로 두고 그 밖의 값도 유지합니다.

After:

> 유연 일정에서는 `startDay`가 0일 때만 null로 바꿉니다. 생략·null과 그 밖의 값은 기존 처리를 유지합니다.

Complete when the edited text retains the supported behavior, conditions, and
evidence scope and satisfies the calling skill's output contract.
