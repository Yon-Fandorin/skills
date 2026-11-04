# Skills

코드베이스 구조 설계, 코드 작성, PR 편집, 작업 마무리와 스킬 검토를 위한 스킬 모음이다.

| 스킬 | 역할 | 호출 |
|------|------|------|
| [Codebase Architecture](codebase-architecture/README.md) | 책임·모듈 배치·의존 경계 설계와 검토 | `$codebase-architecture` |
| [Project Guide](project-guide/SKILL.md) | 프로젝트 파악·유형별 기여 및 관리 지침 선택 | `$project-guide` |
| [Agents Writer](agents-writer/SKILL.md) | 근거에 맞는 간결한 AGENTS.md 작성·정리·검토 | `$agents-writer` |
| [Code Wright](code-wright/README.md) | 코드 작성·리팩터링·검토 | `$code-wright` |
| [PR Writer](pr-writer/README.md) | PR 제목·본문 작성과 편집 | `$pr-writer` |
| [Finish Task](finish-task/SKILL.md) | 완료한 작업의 부산물 정리와 최종 기록 정비 | `$finish-task` |
| [Skill Reviewer](skill-reviewer/README.md) | 독립 에이전트의 스킬 구조·검증 근거 검토 | `$skill-reviewer` |

Project Guide는 프로젝트 지침·관리 체계를 정리할 때 자동 선택될 수 있다. 목적·산출물·작업 흐름을 확인하고 근거가 있는 유형의 지침만 적용한다. 유형이 불확실하면 추측한 기여 규칙은 넣지 않고, 필요한 결정만 질문한다. 유형별 작성법은 별도 참조로 확장한다. 결과물은 프레시 컨텍스트 에이전트의 검수를 받고, 실질적인 개선사항을 반영한 최종본에 미해결 지적이 없어야 완료한다. AGENTS.md 작성·검토는 Agents Writer로 연결한다. Git을 쓰는 프로젝트에서는 PR을 드래프트로 생성하며, CI/CD 추가·활성화·확대는 사용자가 명시적으로 승인한 범위에서만 진행한다.

Agents Writer는 AGENTS.md 작성·정리·검토에 맞으면 자동 선택될 수 있다. 기본 지침은 짧게 유지하고, 판단 보조가 필요할 때만 작성 예시·점검 절차를 읽는다. 공식 출처와 도구별 로딩 차이는 별도 참조로 구분한다.

소프트웨어 유형에서 요청된 구조 설계는 Codebase Architecture, 구현·검증은 Code Wright로 연결한다. Codebase Architecture, Code Wright, PR Writer는 해당 작업에 맞으면 자동 선택될 수 있다. Skill Reviewer는 명시적으로 호출한다. Finish Task는 작업 마무리·부산물 정리 요청에 자동 선택될 수 있으며, 작업 소유권과 기존 승인 범위를 확인하고 최종 기록·참조를 함께 정비한다.

## 설치

공용 Humanizer를 함께 쓰려면 저장소를 `~/.yon-skills`에 받고, [Codex의 사용자 스킬 경로](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)에 연결한다.

```bash
git clone --recurse-submodules https://github.com/Yon-Fandorin/skills.git ~/.yon-skills
mkdir -p ~/.agents/skills
ln -s ~/.yon-skills/codebase-architecture ~/.agents/skills/codebase-architecture
ln -s ~/.yon-skills/project-guide ~/.agents/skills/project-guide
ln -s ~/.yon-skills/agents-writer ~/.agents/skills/agents-writer
ln -s ~/.yon-skills/code-wright ~/.agents/skills/code-wright
ln -s ~/.yon-skills/pr-writer ~/.agents/skills/pr-writer
ln -s ~/.yon-skills/finish-task ~/.agents/skills/finish-task
ln -s ~/.yon-skills/skill-reviewer ~/.agents/skills/skill-reviewer
ln -s ~/.yon-skills/external/humanizer ~/.agents/skills/humanizer
```

설치 후 Codex에서 위 호출 이름을 사용한다. 목록에 나타나지 않으면 Codex를 다시 시작한다.

전체 설치는 PR Writer와 다른 스킬이 고정된 Humanizer를 스킬로 불러올 수 있도록 `humanizer` 링크를 기본으로 포함한다. 설치된 스킬의 이름·설명은 항상 컨텍스트에 포함되므로 그만큼 토큰을 사용한다. Humanizer는 문장 편집 작업에 단독으로 선택될 수도 있다. 텍스트를 붙여 넣어 단독으로 사용하면 초안·남은 패턴·최종 수정본을 반환하고, 다른 스킬이 불러올 때는 해당 스킬의 출력 형식을 따른다.

<details>
<summary>개별 스킬만 설치하기</summary>

공용 Humanizer 없이 각 스킬의 기본 편집 규칙을 사용하려면 [skills CLI](https://github.com/vercel-labs/skills)로 설치할 수 있다. 전체 저장소 설치와 개별 설치 중 하나를 선택한다.

```bash
npx skills@latest add Yon-Fandorin/skills -g -a codex --skill codebase-architecture project-guide agents-writer code-wright pr-writer finish-task skill-reviewer
```

다른 에이전트에서는 `-a codex`를 해당 에이전트 이름으로 바꾸거나, 이 옵션을 빼고 설치 중 선택한다.

</details>

## 업데이트

전체 저장소 설치는 아래 명령으로 스킬과 고정된 Humanizer를 함께 갱신한다. 개별 설치는 `npx skills@latest update`를 사용한다.

```bash
git -C ~/.yon-skills pull --ff-only
git -C ~/.yon-skills submodule update --init --recursive
```

기존 전체 설치에 `humanizer` 링크가 없으면 아래 명령으로 추가한다. 링크가 없어도 다른 스킬은 공유 참조에 따라 고정된 Humanizer 파일을 직접 읽을 수 있다.

```bash
ln -s ~/.yon-skills/external/humanizer ~/.agents/skills/humanizer
```

기존 `codewright` 설치는 [설치](#설치) 안내에 따라 `code-wright`로 다시 연결하거나 설치하고 이전 항목을 제거한다. 심볼릭 링크 설치에서는 저장소를 갱신해도 `~/.agents/skills/codewright` 링크가 자동으로 바뀌지 않는다. 프로젝트 설정 파일 `.codewright.toml`은 계속 사용한다.

## Claude Code

Claude Code에서는 스킬을 Claude Code의 스킬 경로에 연결한다. 연결 범위는 둘 중 하나를 고른다.

**특정 작업 공간만 (권장):** 작업 공간 폴더를 넘겨 스크립트를 실행한다.

```bash
~/.yon-skills/scripts/link-claude-workspace.sh --pr-rule ~/project/my-workspace
```

스크립트는 작업 공간 폴더와 그 아래의 Git 저장소·worktree마다 `.claude/skills`에 이 저장소의 스킬과 `humanizer` 링크를 만들고, 각 저장소의 `.git/info/exclude`에 추가해 커밋되지 않게 한다. Claude Code는 하위 Git 저장소 안에서 상위 폴더의 `.claude/skills`를 읽지 않으므로 저장소마다 링크가 필요하다. 반면 상위 폴더의 `.claude/CLAUDE.md`는 하위 저장소에도 적용되므로, `--pr-rule`은 아래 PR 규칙을 작업 공간 폴더의 `.claude/CLAUDE.md`에 한 번만 추가한다.

작업 공간에 새 저장소나 worktree를 추가하면 같은 명령을 다시 실행한다. 이미 있는 항목은 건너뛰며, `--dry-run`으로 바뀔 내용을 먼저 확인할 수 있다. 작업 공간 밖에 만든 worktree에는 링크와 규칙이 적용되지 않는다.

**모든 프로젝트:** `~/.claude/skills`에 연결하고 사용자 지침(`~/.claude/CLAUDE.md`)에 PR 규칙을 추가한다.

```bash
mkdir -p ~/.claude/skills
for s in agents-writer codebase-architecture code-wright finish-task pr-writer project-guide skill-reviewer; do ln -s ~/.yon-skills/$s ~/.claude/skills/$s; done
ln -s ~/.yon-skills/external/humanizer ~/.claude/skills/humanizer
```

PR 규칙: PR Writer 안의 지시만으로는 Claude가 Humanizer 불러오기를 건너뛰는 경우가 있었다. 이 규칙을 두면 PR을 쓸 때 Humanizer 스킬을 먼저 호출한다.

```text
When writing or revising a pull request title or body, invoke the `humanizer` skill before drafting and apply it in embedded mode to the final text.
```

## Humanizer

문장 편집에는 공용 서브모듈 [Humanizer](https://github.com/blader/humanizer)를 사용한다. 적용 방식과 한국어 편집 기준은 [공통 편집 참조](references/prose-editing.md)를 따른다.

전체 설치는 `humanizer`를 스킬로 함께 연결하므로 `$humanizer`로 단독 호출할 수도 있다.

Claude Code에서 PR을 쓸 때 Humanizer를 안정적으로 쓰게 하는 규칙은 [Claude Code](#claude-code)를 참고한다.

## 관리

에이전트용 지침은 영어, README는 한국어로 작성한다. 한국어 예시와 인용문은 에이전트용 문서에도 넣을 수 있다. 결과물의 언어는 사용자 요청과 대상 저장소의 정책을 따른다.

재사용할 행동 평가 정의와 실행법은 [evals/](evals/README.md)에 두고, 실행 결과·transcript·생성 fixture는 저장소 밖에 보관한다.

문서 작업은 [저장소 지침](AGENTS.md)과 [문서 목록·검토 절차](docs/document-review.md)를 따른다. `lessons.md`에는 재사용할 판단 기준만 남기고, 구체적인 평가 결과·작업 이력은 저장소에 넣지 않는다. 스킬별 실행 규칙과 상세 참조는 각 `SKILL.md`에서 관리한다.
