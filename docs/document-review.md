# 문서 목록과 검토 절차

이 목록은 저장소가 관리하는 파일과 고정된 외부 서브모듈의 파일을 포함한다. 파일 경로와 검토 기준을 유지하며, 특정 작업의 날짜·커밋·검수자·실행 결과를 기록하지 않는다.

## 검토 절차

1. 부모 저장소와 관련 서브모듈의 추적 파일을 각각 열거한다. 숨김 메타데이터와 실행 보조 파일도 포함한다.
2. 변경 파일의 최종 내용을 사용자 요구·저장소 지침·실제 구현 또는 스킬 호출 계약과 대조한다.
3. 내부 링크·frontmatter·UI 메타데이터·명령 예제와 참조의 로딩 조건을 확인한다. 독립 설치를 위해 여러 스킬에 유지하는 공통 정책은 의미가 일치하는지 대조하고, 전체 저장소·개별 설치에서 정책 적용과 참조 로딩이 유지되는지 확인한다.
4. 필요한 검사만 실행하고 구조 검사·내용 검토·행동 평가·실제 서비스 검증의 증거를 구분한다. 미실행 검사를 통과로 표시하지 않는다.
5. 검토 이후 변경한 내용과 영향 경로를 다시 확인한다.

외부 원본은 수정하지 않는다. 패키지·설치 안내 변경이 외부 환경 검사를 필요로 하면 해당 환경에서 확인하거나 미검증 범위를 명시한다. 파일 목록만으로 내용 검토나 행동 평가가 완료된 것은 아니다.

## 파일 목록

| 파일 | 검토할 내용 |
| --- | --- |
| `.gitignore` | 생성 파일·로컬 산출물의 제외 범위 |
| `.gitmodules` | 외부 원본 URL·서브모듈 경로 |
| `AGENTS.md` | 소유·언어·스킬 패키지의 호스트별 메타데이터와 출처·검토 범위·기록 보관 규칙 |
| `README.md` | 역할·호출·설치·예제·현재 문서 연결·Humanizer 기본 링크와 기존 설치 갱신·설명 로딩 비용·단독 호출·Claude Code 작업 공간/전역 설치와 PR 규칙 |
| `agents-writer/SKILL.md` | AGENTS.md 작성·검토·범위·근거·완료 기준 |
| `agents-writer/agents/openai.yaml` | 스킬 이름·표시·호출 정책의 일치 |
| `agents-writer/references/drafting-support.md` | 선택형 작성 보조·근거별 선별·예시·정지 조건 |
| `agents-writer/references/official-guidance.md` | 공식 출처·도구별 로딩 차이·로컬 정책 구분 |
| `codebase-architecture/README.md` | 역할·호출·설치·예제·현재 문서 연결 |
| `codebase-architecture/SKILL.md` | 호출 조건·입력 권위·참조 분기·권한·완료 기준 |
| `codebase-architecture/agents/openai.yaml` | 스킬 이름·표시·prompt·호출 정책의 일치 |
| `codebase-architecture/references/boundary-cases.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `code-wright/README.md` | 역할·호출·설치·예제·현재 문서 연결 |
| `code-wright/SKILL.md` | 호출 조건·입력 권위·참조 분기·권한·완료 기준 |
| `code-wright/agents/openai.yaml` | 스킬 이름·표시·prompt·호출 정책의 일치 |
| `code-wright/fixtures/rust-test-layout/Cargo.toml` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `code-wright/fixtures/rust-test-layout/negative/lib.rs` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `code-wright/fixtures/rust-test-layout/negative/sibling_tests.rs` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `code-wright/fixtures/rust-test-layout/src/lib.rs` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `code-wright/fixtures/rust-test-layout/src/private_logic.rs` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `code-wright/fixtures/rust-test-layout/src/private_logic/tests/calculation.rs` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `code-wright/fixtures/rust-test-layout/src/private_logic/tests/mod.rs` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `code-wright/fixtures/rust-test-layout/src/private_logic/tests/validation.rs` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `code-wright/fixtures/rust-test-layout/tests/public_contract.rs` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `code-wright/references/axum-api-boundaries.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `code-wright/references/cli-project-structure.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `code-wright/references/code-placement-review.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `code-wright/references/default-contribution-rules.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `code-wright/references/lessons.md` | 재사용할 판단 기준·근거 범위; 특정 사례·실행 이력 제외 |
| `code-wright/references/python-code-shape.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `code-wright/references/repository-language-profile.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `code-wright/references/rust-contribution-rules.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `code-wright/references/svelte-component-boundaries.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `code-wright/references/typescript-react-code-shape.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `code-wright/scripts/validate_rust_test_layout.sh` | 실행 조건·결정적 검사·임시 파일·실패 판정 |
| `docs/document-review.md` | 현재 목록의 누락·중복·절차와 저장소 지침의 일치 |
| `dual-agent/README.md` | 역할·두 호스트의 호출·설정·옵션·사전 조건·현재 문서 연결 |
| `dual-agent/SKILL.md` | 명시적 호출 조건·설정 해석 순서·게이트 동작·외부 CLI 실행 규칙·에스컬레이션·완료 기준 |
| `dual-agent/agents/openai.yaml` | 스킬 이름·표시·prompt·호출 정책의 일치 |
| `dual-agent/references/claude-calls.md` | Codex 호스트의 `claude -p` 호출 형태·도구 제한·샌드박스 밖 실행 승인·성공 조건과 SKILL.md의 일치 |
| `dual-agent/references/codex-calls.md` | Claude Code 호스트의 `codex exec` 호출 형태·샌드박스·성공 조건과 SKILL.md의 일치 |
| `dual-agent/references/profile.md` | 프로필 키·기본값·옵션 매핑·첫 사용 절차·검증 규칙과 SKILL.md의 일치 |
| `evals/README.md` | 준비·실행·같은 실행의 필수 조건·dispatch/파일 로딩·설치 불일치 제외·보관 위치·호스트 설정과 격리 한계·Dual Agent stub 경계와 판정 근거 |
| `evals/cases.json` | 선택 경계·비문장 작업의 Humanizer 금지·PR 전용 산출물·기존 PR의 잘못된 주장 수정·edit 후 readback과 메타데이터 보존·파일 대체·docstring만 변경·참조 로딩·수동 의미 판단·환경 전제·stub 필드와 Dual Agent 상태·호출 기록 검사 |
| `evals/fixtures.sh` | 새 fixture 생성·로컬 remote·기존 open draft PR의 저장 상태와 push된 head·로컬 Git 비교 필드·squash와 worktree·사용자 파일 보존 대상·`dual-profile` 프로필 커밋 |
| `evals/run.sh` | Humanizer 링크와 파일 대체 설치·이름/실제 경로/본문 해시·Codex 설치 경로와 내용 비교·사전 확인·환경 제약·중단과 결과 보존·케이스별 stub PATH와 호스트 대체 금지·stub 사전 확인 |
| `evals/score.py` | 실제 stream-json 형태의 합성 주입 fixture·호출/결과/주입 본문 연결·고정 경로와 전체 본문 대조·로딩 출처·설치 불일치 제외·읽기 범위·독립 판정 축·legacy 한계 |
| `evals/bin/gh` | 네트워크 없는 상태 전이·로컬 Git 비교 필드·성공과 실패 기록·jq 필터와 지원 명령 계약 |
| `evals/stubs/codex` | 네트워크 없는 호출 기록·`--version`/`exec` 계약·sandbox별 응답과 fixture 변경·실패 모드 |
| `external/humanizer` | 고정 외부 원본·패키지 연결·로컬 통합 경계 보존 |
| `external/humanizer/.claude-plugin/marketplace.json` | 고정 외부 원본·패키지 연결·로컬 통합 경계 보존 |
| `external/humanizer/.claude-plugin/plugin.json` | 고정 외부 원본·패키지 연결·로컬 통합 경계 보존 |
| `external/humanizer/.cursor-plugin/plugin.json` | 고정 외부 원본·패키지 연결·로컬 통합 경계 보존 |
| `external/humanizer/.github/ISSUE_TEMPLATE/config.yml` | 고정 외부 원본·패키지 연결·로컬 통합 경계 보존 |
| `external/humanizer/.github/ISSUE_TEMPLATE/new-pattern.yml` | 고정 외부 원본·패키지 연결·로컬 통합 경계 보존 |
| `external/humanizer/.github/ISSUE_TEMPLATE/rewrite-problem.yml` | 고정 외부 원본·패키지 연결·로컬 통합 경계 보존 |
| `external/humanizer/.github/workflows/validate.yml` | 고정 외부 원본·패키지 연결·로컬 통합 경계 보존 |
| `external/humanizer/AGENTS.md` | 고정 외부 원본·패키지 연결·로컬 통합 경계 보존 |
| `external/humanizer/CHANGELOG.md` | 고정 외부 원본·패키지 연결·로컬 통합 경계 보존 |
| `external/humanizer/LICENSE` | 고정 외부 원본·패키지 연결·로컬 통합 경계 보존 |
| `external/humanizer/README.md` | 고정 외부 원본·패키지 연결·로컬 통합 경계 보존 |
| `external/humanizer/SKILL.md` | 고정 외부 원본·패키지 연결·로컬 통합 경계 보존 |
| `external/humanizer/agents/openai.yaml` | 고정 외부 원본·패키지 연결·로컬 통합 경계 보존 |
| `external/humanizer/scripts/validate-package.py` | 고정 외부 원본·패키지 연결·로컬 통합 경계 보존 |
| `finish-task/SKILL.md` | 작업 소유권·승인 범위·부산물 정리·최종 기록과 참조·완료 검증 |
| `finish-task/agents/openai.yaml` | 스킬 이름·표시·prompt·호출 정책의 일치 |
| `project-guide/SKILL.md` | 호출 조건·스킬 인계·권한·완료 기준 |
| `project-guide/agents/openai.yaml` | 스킬 이름·표시·호출 정책의 일치 |
| `project-guide/references/completion-review.md` | 프레시 컨텍스트 검수·수정 후 재검수·완료 조건·증거 |
| `project-guide/references/git-workflow.md` | Git 적용 조건·드래프트 PR·CI/CD 명시적 승인·기존 자동화 보존 |
| `project-guide/references/project-types.md` | 유형 선택 조건·미확인 유형·확장 기준 |
| `project-guide/references/project-types/software.md` | 소프트웨어 기여 지침·개발 스킬 연결·검증 범위 |
| `pr-writer/README.md` | 역할·호출·설치·예제·현재 문서 연결 |
| `pr-writer/SKILL.md` | 호출 조건·입력 권위·초안 전 편집 계약 읽기·편집 단계의 Skill 도구 humanizer 호출과 고정 파일 대체·사실 재확인·독립 설치 대체 경로·권한·완료 기준 |
| `pr-writer/agents/openai.yaml` | 스킬 이름·표시·prompt·호출 정책의 일치 |
| `pr-writer/references/editing-examples.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `pr-writer/references/lessons.md` | 재사용할 판단 기준·근거 범위; 특정 사례·실행 이력 제외 |
| `pr-writer/references/publish.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `pr-writer/templates/bugfix.md` | 유형별 검토 질문·선택 섹션·저장소 템플릿 우선 |
| `pr-writer/templates/default.md` | 유형별 검토 질문·선택 섹션·저장소 템플릿 우선 |
| `pr-writer/templates/feature.md` | 유형별 검토 질문·선택 섹션·저장소 템플릿 우선 |
| `pr-writer/templates/hotfix.md` | 유형별 검토 질문·선택 섹션·저장소 템플릿 우선 |
| `pr-writer/templates/infra.md` | 유형별 검토 질문·선택 섹션·저장소 템플릿 우선 |
| `pr-writer/templates/performance.md` | 유형별 검토 질문·선택 섹션·저장소 템플릿 우선 |
| `pr-writer/templates/refactor.md` | 유형별 검토 질문·선택 섹션·저장소 템플릿 우선 |
| `scripts/link-claude-workspace.sh` | 작업 공간과 하위 Git 저장소·worktree 탐색·스킬 목록 자동 수집·기존 항목 보존·info/exclude 추가·PR 규칙 1회 추가·dry-run |
| `references/prose-editing.md` | 고정 원본·humanizer 스킬 실행과 고정 파일 전체 읽기 대체·세션 재사용·embedded mode·호출자 계약·설치/가져오기 금지 |
| `skill-reviewer/README.md` | 역할·호출·설치·예제·현재 문서 연결 |
| `skill-reviewer/SKILL.md` | 호출·독립 검수·실행 근거 검사·판정 범위·미실행 구분 |
| `skill-reviewer/agents/openai.yaml` | 스킬 이름·표시·prompt·호출 정책의 일치 |
| `skill-reviewer/references/exemplars.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `skill-reviewer/references/review-criteria.md` | 작성·호출·실패 사례·검증 근거·비교 주장·판정 기준과 출처 |
