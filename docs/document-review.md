# 문서 전수 검토

문서, 메타데이터, 서브모듈 설정과 실행 보조 파일의 검토 결과를 기록한다.

- 최신 검토: `2026-10-12`, Codewright 첫 사용 설정·검토표 4개 파일, 원본 커밋 `23dbe8469bd55c73b5e84ec63a06fd4f599a969d`
- 최초 전수 검토: `2026-10-12`, 원본 커밋 `b4496738a6960603fa40ab21559edb36206648c5`
- 외부 원본: `blader/humanizer`, `225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8` (`v3.1.0`)
- 최신 검수: Codex 직접 최종 내용 검토·설정 분기 대조·통합 정적 검사. 이전 독립 검수는 아래 기록의 범위에 한정한다.

| 완료 | 파일 | 담당 | 검토 결과 |
|------|------|------|-----------|
| [x] | `.gitignore` | 통합 검증 | 내용 검토 및 기존 파일과 동일함 확인 |
| [x] | `.gitmodules` | 통합 검증 | 공용 경로·원본 URL·서브모듈 설정 확인 |
| [x] | `AGENTS.md` | 통합 검증 | 문서 전수 목록·완료 체크 절차 기록 및 지침 범위 검토 |
| [x] | `README.md` | 독립 검수 | 설치·호출·업데이트 구분, 일반 경로·CLI 안내·공용 편집 연결 확인 |
| [x] | `codewright/README.md` | Codex | 첫 사용·설정 요청 예시·ask/auto 범위·문서 언어·계약 안내 제거 확인 |
| [x] | `codewright/SKILL.md` | Codex | 첫 사용·명시적 재설정·검토 전용 분기·참조 조건·설정 전용 완료 기준 확인 |
| [x] | `codewright/agents/openai.yaml` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `codewright/fixtures/rust-test-layout/Cargo.toml` | 통합 검증 | 내용 검토 및 기존 파일과 동일함 확인 |
| [x] | `codewright/fixtures/rust-test-layout/negative/lib.rs` | 통합 검증 | 내용 검토 및 기존 파일과 동일함 확인 |
| [x] | `codewright/fixtures/rust-test-layout/negative/sibling_tests.rs` | 통합 검증 | 내용 검토 및 기존 파일과 동일함 확인 |
| [x] | `codewright/fixtures/rust-test-layout/src/lib.rs` | 통합 검증 | 내용 검토 및 기존 파일과 동일함 확인 |
| [x] | `codewright/fixtures/rust-test-layout/src/private_logic.rs` | 통합 검증 | 내용 검토 및 기존 파일과 동일함 확인 |
| [x] | `codewright/fixtures/rust-test-layout/src/private_logic/tests/calculation.rs` | 통합 검증 | 내용 검토 및 기존 파일과 동일함 확인 |
| [x] | `codewright/fixtures/rust-test-layout/src/private_logic/tests/mod.rs` | 통합 검증 | 내용 검토 및 기존 파일과 동일함 확인 |
| [x] | `codewright/fixtures/rust-test-layout/src/private_logic/tests/validation.rs` | 통합 검증 | 내용 검토 및 기존 파일과 동일함 확인 |
| [x] | `codewright/fixtures/rust-test-layout/tests/public_contract.rs` | 통합 검증 | 내용 검토 및 기존 파일과 동일함 확인 |
| [x] | `codewright/references/axum-api-boundaries.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `codewright/references/cli-project-structure.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `codewright/references/code-placement-review.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `codewright/references/default-contribution-rules.md` | 언어 지침 | 주석·API 문서·테스트 설명 언어 기준 명시 |
| [x] | `codewright/references/lessons.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `codewright/references/python-code-shape.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `codewright/references/repository-language-profile.md` | Codex | 초기 질문·저장 권한·누락 기본값·기존 규칙 우선·TOML 예시 파싱 확인 |
| [x] | `codewright/references/rust-contribution-rules.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `codewright/references/svelte-component-boundaries.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `codewright/references/typescript-react-code-shape.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `codewright/scripts/validate_rust_test_layout.sh` | 통합 검증 | 내용 검토 및 기존 파일과 동일함 확인 |
| [x] | `docs/document-review.md` | Codex | 목록 62행·변경 4개 파일·직접 검토·정적 검사와 미실행 범위 대조 |
| [x] | `external/humanizer` | 통합 검증 | Git 서브모듈 경로·고정 커밋·원본 보존 확인 |
| [x] | `external/humanizer/.claude-plugin/marketplace.json` | 외부 원본 | 검토 완료·고정 커밋의 원본과 동일 |
| [x] | `external/humanizer/.claude-plugin/plugin.json` | 외부 원본 | 검토 완료·고정 커밋의 원본과 동일 |
| [x] | `external/humanizer/.cursor-plugin/plugin.json` | 외부 원본 | 검토 완료·고정 커밋의 원본과 동일 |
| [x] | `external/humanizer/.github/ISSUE_TEMPLATE/config.yml` | 외부 원본 | 검토 완료·고정 커밋의 원본과 동일 |
| [x] | `external/humanizer/.github/ISSUE_TEMPLATE/new-pattern.yml` | 외부 원본 | 검토 완료·고정 커밋의 원본과 동일 |
| [x] | `external/humanizer/.github/ISSUE_TEMPLATE/rewrite-problem.yml` | 외부 원본 | 검토 완료·고정 커밋의 원본과 동일 |
| [x] | `external/humanizer/.github/workflows/validate.yml` | 외부 원본 | 검토 완료·고정 커밋의 원본과 동일 |
| [x] | `external/humanizer/AGENTS.md` | 외부 원본 | 검토 완료·고정 커밋의 원본과 동일 |
| [x] | `external/humanizer/CHANGELOG.md` | 외부 원본 | 검토 완료·고정 커밋의 원본과 동일 |
| [x] | `external/humanizer/LICENSE` | 외부 원본 | 검토 완료·고정 커밋의 원본과 동일 |
| [x] | `external/humanizer/README.md` | 외부 원본 | 검토 완료·고정 커밋의 원본과 동일 |
| [x] | `external/humanizer/SKILL.md` | 외부 원본 | 검토 완료·고정 커밋의 원본과 동일 |
| [x] | `external/humanizer/agents/openai.yaml` | 외부 원본 | 검토 완료·고정 커밋의 원본과 동일 |
| [x] | `external/humanizer/scripts/validate-package.py` | 외부 원본 | 검토 완료·고정 커밋의 원본과 동일 |
| [x] | `pr-writer/README.md` | README 검수 | 소개·호출 예시·작성과 게시 범위·상세 지침 링크 확인 |
| [x] | `pr-writer/SKILL.md` | 언어 지침 | 공용 편집·단독 설치 대체 처리·PR 언어 정리 |
| [x] | `pr-writer/agents/openai.yaml` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `pr-writer/references/editing-examples.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `pr-writer/references/lessons.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `pr-writer/references/publish.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `pr-writer/templates/bugfix.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `pr-writer/templates/default.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `pr-writer/templates/feature.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `pr-writer/templates/hotfix.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `pr-writer/templates/infra.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `pr-writer/templates/performance.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `pr-writer/templates/refactor.md` | 언어 지침 | 언어·형식·참조 검토 완료·내용 유지 |
| [x] | `references/prose-editing.md` | 언어 지침 | 공용 경로 해석·한국어 편집·의미 보존 정리 |
| [x] | `skill-reviewer/README.md` | 독립 검수 | 독립 검수·원문 참조·읽기 전용·세 가지 판정 상태 확인 |
| [x] | `skill-reviewer/SKILL.md` | 독립 검수 | fresh dispatch·원문 보정·전 축 검수·caller 대조·미완료 상태 확인 |
| [x] | `skill-reviewer/agents/openai.yaml` | 독립 검수 | 새 검수 방식과 UI 문구 일치, 명시적 호출 정책 유지 |
| [x] | `skill-reviewer/references/exemplars.md` | 독립 검수 | 필수 원문 읽기·유형별 선택·출처 기록·참조 미완료 처리 확인 |
| [x] | `skill-reviewer/references/review-criteria.md` | 독립 검수 | 전 축 및 검토 범위·출처·독립성·미완료 근거 확인 |

완료: **62/62**. 완료 표시는 직접 검수한 최종 파일과 적용 가능한 검사 결과를 대조한 항목에만 부여했다.

## Codewright 첫 사용 설정 검증

검토자는 Codex이며, 변경한 `codewright/SKILL.md`, `codewright/README.md`, `codewright/references/repository-language-profile.md`, 이 검토표를 직접 읽고 대조했다. 원본 커밋은 `23dbe8469bd55c73b5e84ec63a06fd4f599a969d`다. 수정하지 않은 파일의 완료 표시는 이전 검토 결과를 유지한다. 사용자의 범위 조정에 따라 이번에 추가했던 계약 문서 참조·작성 지침·설정 예시를 제거했다. 첫 사용 언어 설정과 `ask`/`auto` 안내는 유지한다.

설정 없음·설정 건너뛰기/미응답·기존 설정·명시적 저장 요청·검토 전용·저장소 규칙 충돌·잘못된 프로필 분기를 지침으로 대조했다. 코드 언어 세 항목과 문서 언어를 구분하고, `ask`/`auto`가 배치 승인만 바꾸는지 확인했다. 이미 결정한 설정에 재승인을 요구하지 않고 미응답은 저장 허가로 취급하지 않도록 확인했다.

스킬 기본 검증과 `git diff --check`가 통과했다. 변경한 문서의 내부 링크 16개와 TOML 규격 예시 1개를 확인했고, 기존 UI의 명시적 호출 정책을 유지했다. 부모 저장소의 추적 파일과 서브모듈의 추적 파일을 각각 열거해 목록 62행의 중복·누락이 없음을 확인했다. 외부 원본 14개에는 숨김 메타데이터도 포함한다. 이번 외부 검사는 고정 커밋과 작업 트리 보존만 확인했으며, 외부 파일의 내용을 재검토하거나 upstream 패키지 검증을 다시 실행하지 않았다.

AI Hero의 [설정 안내](https://www.aihero.dev/skills-setup-matt-pocock-skills)와 [`setup-matt-pocock-skills` 원문](https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/SKILL.md)을 `2026-10-12`에 읽고 저장소별 설정 방식을 참고했다. 이슈 트래커·라벨·Claude 우선 파일 선택은 도입하지 않았다. TOML 규격과 `ask`/`auto`는 이 저장소의 규칙이다.

새 에이전트로 실제 첫 사용 대화를 실행하거나 소비 저장소에 설정 파일을 저장하는 행동 검증은 실행하지 않았다. 독립 검수, Rust fixture 재컴파일, 외부 설치·게시도 이번 검증 범위에 포함하지 않는다. 위 결과는 최종 문서의 구조·권한·링크·메타데이터 일관성을 확인하며 모든 실행 환경에서 같은 동작을 보장하지 않는다.

## Skill Reviewer·설치 안내 검증

새 컨텍스트 워커가 AI Hero의 `writing-for-agents`, `SKILL-MECHANICS.md`, `code-review` 원문을 읽고 7개 검토 축과 설치 README를 대조해 `Ready`로 판정했다. 원문 스냅샷은 `mattpocock/skills`의 `49dd158d1076134a641b33efb035946536778336`에서 받았다.

별도 실행 검증에서는 caller가 `fork_turns: "none"`으로 새 워커 하나를 생성했다. 워커는 작성 이력 없이 자료를 읽고, 릴리스 노트 샘플의 읽기 전용 계약과 게시 단계 간 충돌을 Major로 식별했다. caller가 지적 위치·원문 읽기·스냅샷을 대조했다. 위임 불가·원문 접근 불가 경로는 지침 검수로 확인했으며 실제 장애 환경에서 실행하지 않았다.

내부 링크 12개, Bash 블록 3개, 프런트매터·UI 호출 정책·문서 자동 검사와 전체 목록 62행을 확인했다. 별도 임시 디렉터리에서 설치·업데이트 명령을 실행해 세 스킬 연결과 공용 편집 경로를 확인했다. 이 검증은 로컬 Git 원본·캐시된 서브모듈 객체를 사용했다. 원격 신규 복제, CLI 실제 설치, 사용자 설정 변경은 실행하지 않았다.

설치 안내는 [누적 설치 순위](https://www.skills.sh/)와 [트렌딩](https://www.skills.sh/trending)을 대조하고 [Vercel Skills](https://github.com/vercel-labs/skills), [Matt Pocock](https://github.com/mattpocock/skills), [Agent Browser](https://github.com/vercel-labs/agent-browser), [Anthropic](https://github.com/anthropics/skills), [HyperFrames](https://github.com/heygen-com/hyperframes)의 README 및 [Codex 공식 문서](https://developers.openai.com/codex/skills/#where-to-save-skills)를 확인했다. 순위는 검토 시점의 참고 근거다.

## 이전 README 축약 검증

원본 커밋: `fd40710b27d1d4cd33dcd4da2bb51427aed904a2`.

네 README의 최종 내용을 현재 지침·호출 정책과 대조하고 별도 검수에서 `Ready` 판정을 받았다. 내부 링크 13개, 설치 명령 두 블록의 Bash 문법, 문서 자동 검사와 전체 목록 62행의 일치를 확인했다. 설치 명령은 실행하지 않았다.

수정하지 않은 파일은 기존 검토 결과를 유지한다. 아래 기록은 당시 검증 범위이며 현재 작업에서 모두 다시 실행하지 않았다.

## 최초 전수 검증

외부 14개 파일은 고정 커밋의 원본을 유지하고 패키지 검증을 통과했다. 공용 경로의 직접 설치·심볼릭 링크·단독 설치·서브모듈 누락 사례를 확인했다.

세 스킬의 프런트매터와 기존 UI 호출 정책을 확인했다. 별도 프레시 컨텍스트 통합 검수는 일반 파일 61개, 내부 링크 53개, 세 스킬의 경로 사례 27개를 확인하고 `Ready`로 판정했다. Git 서브모듈 경로·고정 커밋·공개 원본 URL과 별도 복제본의 등록·초기화를 확인했다.

복제본 초기화에는 로컬에 이미 받은 Git 객체를 사용했으며 공개 원본 URL 등록을 확인했다. upstream 네트워크에서 새로 받는 작업은 실행하지 않았다. 자동 문서 검사는 기존 `codewright/references/lessons.md`의 제목 다음 도입 문단에 대한 문체 알림 1건을 남겼다. 내용·언어 정책·링크 결함으로 판단하지 않아 유지했다.

Rust fixture와 검사 스크립트는 기존 검증한 원본과 동일하며 이번 작업에서 다시 컴파일하지 않았다. 외부 CLI 설치·운영 조회·원격 PR 게시도 이번 검수에서 실행하지 않았다.

## 다음 문서 작업

[저장소 지침](../AGENTS.md)에 따라 파일 목록을 갱신한다. 추가·수정·이동한 파일은 완료를 해제하고, 최종 내용과 적용 가능한 검사 결과를 확인한 뒤 다시 체크한다. 검토 시점의 완료 기록을 이후 편집에 그대로 적용하지 않는다.
