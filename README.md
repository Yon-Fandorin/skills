# Skills

코드베이스 구조 설계, 코드 작성, PR 편집과 스킬 검토를 위한 스킬 모음이다.

| 스킬 | 역할 | 호출 |
|------|------|------|
| [Codebase Architecture](codebase-architecture/README.md) | 책임·모듈 배치·의존 경계 설계와 검토 | `$codebase-architecture` |
| [Project Guide](project-guide/SKILL.md) | 프로젝트 파악·유형별 기여 및 관리 지침 선택 | `$project-guide` |
| [Agents Writer](agents-writer/SKILL.md) | 근거에 맞는 간결한 AGENTS.md 작성·정리·검토 | `$agents-writer` |
| [Code Wright](code-wright/README.md) | 코드 작성·리팩터링·검토 | `$code-wright` |
| [PR Writer](pr-writer/README.md) | PR 제목·본문 작성과 편집 | `$pr-writer` |
| [Skill Reviewer](skill-reviewer/README.md) | 독립 에이전트의 스킬 구조 검토 | `$skill-reviewer` |

Project Guide는 프로젝트 지침·관리 체계를 정리할 때 자동 선택될 수 있다. 목적·산출물·작업 흐름을 확인하고 근거가 있는 유형의 지침만 적용한다. 유형이 불확실하면 추측한 기여 규칙은 넣지 않고, 필요한 결정만 질문한다. 유형별 작성법은 별도 참조로 확장한다. 결과물은 프레시 컨텍스트 에이전트의 검수를 받고, 실질적인 개선사항을 반영한 최종본에 미해결 지적이 없어야 완료한다. AGENTS.md 작성·검토는 Agents Writer로 연결한다. Git을 쓰는 프로젝트에서는 PR을 드래프트로 생성하며, CI/CD 추가·활성화·확대는 사용자가 명시적으로 승인한 범위에서만 진행한다.

Agents Writer는 AGENTS.md 작성·정리·검토에 맞으면 자동 선택될 수 있다. 기본 지침은 짧게 유지하고, 판단 보조가 필요할 때만 작성 예시·점검 절차를 읽는다. 공식 출처와 도구별 로딩 차이는 별도 참조로 구분한다.

소프트웨어 유형에서 요청된 구조 설계는 Codebase Architecture, 구현·검증은 Code Wright로 연결한다. Codebase Architecture와 PR Writer는 해당 작업에 맞으면 자동 선택될 수 있다. Code Wright와 Skill Reviewer는 명시적으로 호출한다.

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
ln -s ~/.yon-skills/skill-reviewer ~/.agents/skills/skill-reviewer
```

설치 후 Codex에서 위 호출 이름을 사용한다. 목록에 나타나지 않으면 Codex를 다시 시작한다.

<details>
<summary>개별 스킬만 설치하기</summary>

공용 Humanizer 없이 각 스킬의 기본 편집 규칙을 사용하려면 [skills CLI](https://github.com/vercel-labs/skills)로 설치할 수 있다. 전체 저장소 설치와 개별 설치 중 하나를 선택한다.

```bash
npx skills@latest add Yon-Fandorin/skills -g -a codex --skill codebase-architecture project-guide agents-writer code-wright pr-writer skill-reviewer
```

다른 에이전트에서는 `-a codex`를 해당 에이전트 이름으로 바꾸거나, 이 옵션을 빼고 설치 중 선택한다.

</details>

## 업데이트

전체 저장소 설치는 아래 명령으로 스킬과 고정된 Humanizer를 함께 갱신한다. 개별 설치는 `npx skills@latest update`를 사용한다.

```bash
git -C ~/.yon-skills pull --ff-only
git -C ~/.yon-skills submodule update --init --recursive
```

기존 `codewright` 설치는 [설치](#설치) 안내에 따라 `code-wright`로 다시 연결하거나 설치하고 이전 항목을 제거한다. 심볼릭 링크 설치에서는 저장소를 갱신해도 `~/.agents/skills/codewright` 링크가 자동으로 바뀌지 않는다. 프로젝트 설정 파일 `.codewright.toml`은 계속 사용한다.

## Humanizer

문장 편집에는 공용 서브모듈 [Humanizer](https://github.com/blader/humanizer)를 사용한다. 적용 방식과 한국어 편집 기준은 [공통 편집 참조](references/prose-editing.md)를 따른다.

`$humanizer`로 단독 호출하려면 `~/.yon-skills/external/humanizer`도 도구의 스킬 경로에 연결한다.

## 관리

에이전트용 지침은 영어, README는 한국어로 작성한다. 한국어 예시와 인용문은 에이전트용 문서에도 넣을 수 있다. 결과물의 언어는 사용자 요청과 대상 저장소의 정책을 따른다.

문서 작업은 [저장소 지침](AGENTS.md)과 [문서 목록·검토 절차](docs/document-review.md)를 따른다. `lessons.md`에는 재사용할 판단 기준을 남기고, 구체적인 평가·작업 이력은 버전 관리에서 제외한 로컬 기록에 보관한다. 스킬별 실행 규칙과 상세 참조는 각 `SKILL.md`에서 관리한다.
