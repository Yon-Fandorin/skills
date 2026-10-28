# 문서 목록과 검토 절차

이 목록은 저장소가 관리하는 파일과 고정된 외부 서브모듈의 파일을 포함한다. 파일 경로와 검토 기준을 유지하며, 특정 작업의 날짜·커밋·검수자·실행 결과를 기록하지 않는다.

## 검토 절차

1. 부모 저장소와 관련 서브모듈의 추적 파일을 각각 열거한다. 숨김 메타데이터와 실행 보조 파일도 포함한다.
2. 변경 파일의 최종 내용을 사용자 요구·저장소 지침·실제 구현 또는 스킬 호출 계약과 대조한다.
3. 내부 링크·frontmatter·UI 메타데이터·명령 예제와 참조의 로딩 조건을 확인한다.
4. 필요한 검사만 실행하고 구조 검사·내용 검토·행동 평가·실제 서비스 검증의 증거를 구분한다. 미실행 검사를 통과로 표시하지 않는다.
5. 검토 이후 변경한 내용과 영향 경로를 다시 확인한다. 실제 검토 범위·출처·판정·제한은 버전 관리에서 제외한 로컬 기록에 보관한다.

외부 원본은 수정하지 않는다. 패키지·설치 안내 변경이 외부 환경 검사를 필요로 하면 해당 환경에서 확인하거나 미검증 범위를 명시한다. 파일 목록만으로 내용 검토나 행동 평가가 완료된 것은 아니다.

## 파일 목록

| 파일 | 검토할 내용 |
| --- | --- |
| `.gitignore` | 생성 파일·로컬 산출물의 제외 범위 |
| `.gitmodules` | 외부 원본 URL·서브모듈 경로 |
| `AGENTS.md` | 소유·언어·검토 범위·기록 보관 규칙 |
| `README.md` | 역할·호출·설치·예제·현재 문서 연결 |
| `agents-writer/SKILL.md` | AGENTS.md 작성·검토·범위·근거·완료 기준 |
| `agents-writer/agents/openai.yaml` | 스킬 이름·표시·호출 정책의 일치 |
| `agents-writer/references/drafting-support.md` | 선택형 작성 보조·근거별 선별·예시·정지 조건 |
| `agents-writer/references/official-guidance.md` | 공식 출처·도구별 로딩 차이·로컬 정책 구분 |
| `codebase-architecture/README.md` | 역할·호출·설치·예제·현재 문서 연결 |
| `codebase-architecture/SKILL.md` | 호출 조건·입력 권위·참조 분기·권한·완료 기준 |
| `codebase-architecture/agents/openai.yaml` | 스킬 이름·표시·prompt·호출 정책의 일치 |
| `codebase-architecture/references/boundary-cases.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `codewright/README.md` | 역할·호출·설치·예제·현재 문서 연결 |
| `codewright/SKILL.md` | 호출 조건·입력 권위·참조 분기·권한·완료 기준 |
| `codewright/agents/openai.yaml` | 스킬 이름·표시·prompt·호출 정책의 일치 |
| `codewright/fixtures/rust-test-layout/Cargo.toml` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `codewright/fixtures/rust-test-layout/negative/lib.rs` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `codewright/fixtures/rust-test-layout/negative/sibling_tests.rs` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `codewright/fixtures/rust-test-layout/src/lib.rs` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `codewright/fixtures/rust-test-layout/src/private_logic.rs` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `codewright/fixtures/rust-test-layout/src/private_logic/tests/calculation.rs` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `codewright/fixtures/rust-test-layout/src/private_logic/tests/mod.rs` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `codewright/fixtures/rust-test-layout/src/private_logic/tests/validation.rs` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `codewright/fixtures/rust-test-layout/tests/public_contract.rs` | 실제 테스트 발견·공개/비공개 접근 계약 |
| `codewright/references/axum-api-boundaries.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `codewright/references/cli-project-structure.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `codewright/references/code-placement-review.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `codewright/references/default-contribution-rules.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `codewright/references/lessons.md` | 재사용할 판단 기준·근거 범위; 특정 사례·실행 이력 제외 |
| `codewright/references/python-code-shape.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `codewright/references/repository-language-profile.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `codewright/references/rust-contribution-rules.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `codewright/references/svelte-component-boundaries.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `codewright/references/typescript-react-code-shape.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `codewright/scripts/validate_rust_test_layout.sh` | 실행 조건·결정적 검사·임시 파일·실패 판정 |
| `docs/document-review.md` | 현재 목록의 누락·중복·절차와 저장소 지침의 일치 |
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
| `pr-writer/README.md` | 역할·호출·설치·예제·현재 문서 연결 |
| `pr-writer/SKILL.md` | 호출 조건·입력 권위·참조 분기·권한·완료 기준 |
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
| `references/prose-editing.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `skill-reviewer/README.md` | 역할·호출·설치·예제·현재 문서 연결 |
| `skill-reviewer/SKILL.md` | 호출 조건·입력 권위·참조 분기·권한·완료 기준 |
| `skill-reviewer/agents/openai.yaml` | 스킬 이름·표시·prompt·호출 정책의 일치 |
| `skill-reviewer/references/exemplars.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
| `skill-reviewer/references/review-criteria.md` | 본문의 역할·관련 SKILL 참조 조건·권한·완료 기준 |
