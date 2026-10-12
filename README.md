# Skills

코드 작성, PR 편집, 스킬 검토를 위한 스킬 모음이다.

| 스킬 | 역할 | 호출 |
|------|------|------|
| [Codewright](codewright/README.md) | 코드 작성·리팩터링·검토 | `$codewright` |
| [PR Writer](pr-writer/README.md) | PR 제목·본문 작성과 편집 | `$pr-writer` |
| [Skill Reviewer](skill-reviewer/README.md) | 독립 에이전트의 스킬 구조 검토 | `$skill-reviewer` |

Codewright와 Skill Reviewer는 명시적으로 호출한다. PR Writer는 작업에 맞으면 자동 선택될 수 있다.

## 설치

공용 Humanizer를 함께 쓰려면 저장소를 `~/.yon-skills`에 받고, [Codex의 사용자 스킬 경로](https://developers.openai.com/codex/skills/#where-to-save-skills)에 연결한다.

```bash
git clone --recurse-submodules https://github.com/Yon-Fandorin/skills.git ~/.yon-skills
mkdir -p ~/.agents/skills
ln -s ~/.yon-skills/codewright ~/.agents/skills/codewright
ln -s ~/.yon-skills/pr-writer ~/.agents/skills/pr-writer
ln -s ~/.yon-skills/skill-reviewer ~/.agents/skills/skill-reviewer
```

설치 후 Codex에서 위 호출 이름을 사용한다. 목록에 나타나지 않으면 Codex를 다시 시작한다.

<details>
<summary>개별 스킬만 설치하기</summary>

공용 Humanizer 없이 각 스킬의 기본 편집 규칙을 사용하려면 [skills CLI](https://github.com/vercel-labs/skills)로 설치할 수 있다. 전체 저장소 설치와 개별 설치 중 하나를 선택한다.

```bash
npx skills@latest add Yon-Fandorin/skills -g -a codex --skill codewright pr-writer skill-reviewer
```

다른 에이전트에서는 `-a codex`를 해당 에이전트 이름으로 바꾸거나, 이 옵션을 빼고 설치 중 선택한다.

</details>

## 업데이트

전체 저장소 설치는 아래 명령으로 스킬과 고정된 Humanizer를 함께 갱신한다. 개별 설치는 `npx skills@latest update`를 사용한다.

```bash
git -C ~/.yon-skills pull --ff-only
git -C ~/.yon-skills submodule update --init --recursive
```

## Humanizer

문장 편집에는 공용 서브모듈 [Humanizer](https://github.com/blader/humanizer)를 사용한다. 적용 방식과 한국어 편집 기준은 [공통 편집 참조](references/prose-editing.md)를 따른다.

`$humanizer`로 단독 호출하려면 `~/.yon-skills/external/humanizer`도 도구의 스킬 경로에 연결한다.

## 관리

에이전트용 지침은 영어, README는 한국어로 작성한다. 한국어 예시와 인용문은 에이전트용 문서에도 넣을 수 있다. 결과물의 언어는 사용자 요청과 대상 저장소의 정책을 따른다.

문서 작업은 [저장소 지침](AGENTS.md)을 따르고 [전수 검토표](docs/document-review.md)에 완료 여부를 기록한다. 스킬별 실행 규칙과 상세 참조는 각 `SKILL.md`에서 관리한다.
