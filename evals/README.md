# 행동 평가

스킬의 선택 경계, 참조 로딩, 작업 결과를 반복해서 확인한다. 재사용할 정의는 이 디렉터리에 두고 실행 결과·transcript·생성 fixture는 저장소 밖에 보관한다. 개별 스킬 설치에는 평가 도구를 포함하지 않는다.

## 준비

Bash, Git, Python 3.10 이상과 실행할 호스트 CLI(`claude` 또는 `codex`), 해당 호스트의 인증이 필요하다. Python 추가 패키지는 사용하지 않는다. 전체 설치의 참조 로딩을 평가하려면 고정된 `external/humanizer` 서브모듈도 준비한다. fixture 테스트는 Python 표준 라이브러리 `unittest`로 실행한다.

gh의 `--jq` 또는 `-q` 필터를 쓰는 실행에는 PATH에서 찾을 수 있는 `jq`도 필요하다. 없으면 stub이 이유를 기록하고 해당 호출을 실패로 반환한다.

Claude Code의 `full` 설치는 fixture의 `.claude/skills/`에 이 checkout의 스킬을 심볼릭 링크로 연결하며, `humanizer`는 `external/humanizer`를 가리킨다. `full-no-humanizer-skill`은 이 링크만 생략해 파일 대체 경로를 평가한다. `pr-standalone`은 `pr-writer` 하나만 실제 디렉터리로 복사한다. `metadata.json`의 `installed_skills`에 각 스킬의 이름·실제 경로·파일 해시·frontmatter를 제외한 본문 해시(`body_sha256`)를 기록한다. 본문 해시는 양끝 공백을 제외한 UTF-8 텍스트 기준이다. Claude 실행은 `--setting-sources project,local`로 사용자 범위의 설정·CLAUDE.md·스킬을 불러오지 않는다. 이 옵션이 다루지 않는 범위는 여전히 영향을 줄 수 있다. Claude 도구 허용 목록은 케이스별 profile에 명시한다. 허용 목록 자체가 파일시스템 sandbox는 아니다.

Codex는 사용자의 기존 스킬 설치를 그대로 사용한다. 실행 전에 [공식 사용자 스킬 경로](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)인 `~/.agents/skills`에서 `pr-writer`, `code-wright`, `humanizer`의 실제 경로와 파일 내용을 checkout과 비교한다. 앞의 두 스킬의 실제 디렉터리를 기준으로 찾은 `references/prose-editing.md`도 각각 비교한다. `installation_check`에 항목별 경로·해시·일치 여부·읽기 오류를 기록한다. 누락이나 경로·내용 불일치가 있으면 호스트 실행 결과는 보존하되 채점 보고서 전체 상태를 `install_mismatch`, `regression_eligible`을 `false`로 표시해 회귀 판단에서 제외한다. 일치할 때는 `installation_check.status`가 `match`다. 다른 스킬 scope·플러그인·비활성화 설정과 실제 선택 경로까지 증명하는 검사는 아니므로 설치 일치와 행동 증거를 함께 검토한다. 독립 설치와 Claude 전용 자동 호출 정책 케이스는 Claude에서만 실행한다. 평가를 위해 사용자 전역 설정을 수정하지 않는다.

## 생성·실행·채점

저장소 루트에서 실행한다. 먼저 호스트 없이 fixture를 만들고 살펴볼 수 있다. 목적지는 존재하지 않는 저장소 밖 경로여야 한다.

```bash
fixture_parent=$(mktemp -d)
bash evals/fixtures.sh finish "$fixture_parent/fixture"
git -C "$fixture_parent/fixture" worktree list
(cd "$fixture_parent/fixture" && python3 -m unittest discover -s tests)
```

실행기의 인자는 호스트, 케이스 ID, 반복 ID, 선택적인 새 출력 경로다. 출력 경로를 생략하면 시스템 임시 디렉터리의 `skills-evals/` 아래에 UTC 시각·케이스·임의 접미사를 가진 새 디렉터리를 만든다. 기존 디렉터리는 비어 있어도 덮어쓰지 않는다. 시작할 때 출력 경로를 표시한다.

```bash
bash evals/run.sh claude pr-publish 1
bash evals/run.sh claude pr-draft-file-fallback 1
bash evals/run.sh codex doc-edit 1
bash evals/run.sh codex refactor-approval 1
EVAL_MODEL=sonnet EVAL_TIMEOUT=600 bash evals/run.sh claude agents-cleanup 2
EVAL_REASONING_EFFORT=high bash evals/run.sh codex bug-fix 2
python3 evals/score.py /path/to/new-run
```

기본 모델 요청은 Claude `sonnet`, Codex `gpt-6.1-sol`이며 `EVAL_MODEL`로 바꾼다. 이 값은 요청값이다. CLI가 실제 모델 ID를 transcript에 노출하지 않으면 관측값은 `unknown`이다. 기본 제한 시간은 900초이고 `EVAL_TIMEOUT`으로 초 단위 설정한다. timeout·오류·중단 시 부분 transcript와 실행 상태를 보존하며 실행기는 실패로 종료한다. 자식 프로세스 그룹도 종료한다.

Codex reasoning effort는 `EVAL_REASONING_EFFORT`로 정하며 기본값은 `high`다. 실행기는 `-c model_reasoning_effort=...`로 명시하고 메타데이터의 `reasoning_effort`에 기록한다. Claude에는 effort 플래그를 추가하지 않으며 `host-default`로 기록한다. Claude 실행에는 이 환경변수를 적용하지 않는다.

출력에는 정의 사본, prompt, 메타데이터, 참조 원문 사본, 초기·최종 파일/Git 스냅샷, gh 호출/상태, transcript와 stderr, 실행 상태, fixture가 남는다. 메타데이터는 checkout 커밋과 dirty 여부, Humanizer 실제 커밋과 gitlink, 정의 해시, CLI 버전, 모델, 권한·도구·설치 설정을 담는다. 비밀이 담길 수 있는 전체 환경변수나 사용자 설정 파일은 복사하지 않는다. fixture와 로그의 내용은 호스트 행동에 따라 달라지므로 결과 공유 전 내용을 확인한다. Claude는 실행 위치마다 `~/.claude/projects/` 아래에 기록 폴더를 만들므로, fixture 경로로 생긴 기록은 평가 후 필요 없으면 지운다.

기존 transcript만 읽을 때는 호스트와 케이스를 지정한다.

```bash
python3 evals/score.py --legacy /path/to/transcript.jsonl --host claude --case pr-draft
python3 evals/score.py --legacy /path/to/transcript.jsonl --host codex --case pr-publish
python3 evals/score.py --self-check
```

legacy 모드는 현재 checkout의 참조 원문을 비교 보조로 사용한다. 과거 실행의 원문 revision이나 fixture 최종 상태를 복원하지 않는다. 스냅샷·stub 로그가 없는 항목과 하위 에이전트 내부 증거가 빠진 항목은 `unknown`으로 남긴다. 설치 일치 기록이 없는 Codex 결과도 회귀 판단에서 제외한다. JSON 보고서는 stdout으로 반환하며 저장하려면 저장소 밖으로 리다이렉트한다. 채점 명령의 정상 종료는 보고서 생성 성공을 뜻하며 평가 통과는 보고서의 `status`로 확인한다.

## 케이스와 판정

[cases.json](cases.json)의 `schema_version`은 1이다. `profiles`는 sandbox·Claude permission mode·허용 도구를 정의하고, 각 케이스는 `id`, `prompt`, `fixture`, `hosts`, `profile`, `installation`, `checks`, `expected`를 가진다.

| 케이스 | 확인할 행동 |
| --- | --- |
| `agents-cleanup` | AGENTS.md 정리는 agents-writer 선택 |
| `project-guidance` | project-guide와 agents-writer 선택, 실제 fresh-context 하위 에이전트 검수와 검수자 기록 |
| `architecture-review` | codebase-architecture 선택, 수정 없이 구조 검토 |
| `bug-fix` | 한 줄 버그 수정도 code-wright 선택, 산술 동작 복구 |
| `refactor-approval` | code-wright 선택, 구조 판단을 위한 codebase-architecture 로딩 허용, 구조 제안 뒤 승인 전 정지·수정 없음 |
| `finish-cleanup` | finish-task 선택, 지정 부산물 정리·사용자 작업 보존·squash 내용 확인·worktree 등록 제거·최종 기록 정비 |
| `pr-draft` | pr-writer 선택, 같은 실행에서 공유 참조 전체와 Humanizer 로딩, PR만 반환 |
| `pr-draft-file-fallback` | Claude에서 humanizer 링크 없이 고정 파일 전체 로딩, 참고 결과로 보고 |
| `doc-edit` | 두 호스트에서 code-wright 선택·Humanizer 로딩·build_invoice docstring만 변경·의미 보존 |
| `explain-code` | 설명 요청은 대상 스킬 자동 선택 없음 |
| `general-review` | 일반 코드 리뷰는 code-wright 자동 선택 없음 |
| `implementation-finish` | 구현 마무리는 code-wright 선택, finish-task 선택 없음 |
| `skill-readiness` | Claude의 일반 준비도 검토는 skill-reviewer를 Skill로 자동 호출하지 않음(저장소 파일로 읽는 것은 허용) |
| `pr-publish` | 같은 실행에서 공유 참조 전체와 Humanizer 로딩·draft 게시·기존 유형 라벨·readback·ready 금지·반환/게시 본문에 PR만 포함 |
| `pr-revise` | 기존 draft PR의 잘못된 주장을 현재 diff·검증 근거에 맞게 수정·공유 참조와 Humanizer 전체 로딩·edit 후 readback·base/head/라벨/draft 보존·create/ready 금지·PR만 반환/게시 |
| `pr-standalone` | 독립 pr-writer 복사본은 의존성 탐색 없이 기본 편집 완료 |

`expected`의 판정 표면은 다음과 같다. 알 수 없는 상태/gh 연산은 채점 오류로 처리한다.

| 필드 | 정의 |
| --- | --- |
| `selection` | `required`와 `forbidden` 스킬 이름 목록; `inspection_only`는 검토 대상 SKILL 읽기를 선택에서 제외하며 실제 Skill dispatch는 제외하지 않음 |
| `references` | `path`와 `coverage: full`; 여러 읽기의 실제 반환 범위를 합산. 선택적 `load_source`는 `file_read` 또는 `skill_dispatch`로 증거를 제한 |
| `file_state` | `unchanged(paths)`, `absent(paths)`, `changed(path)`, `branch_absent(name)`, `branch_unchanged(name)`, `worktree_absent(path)` |
| `gh_calls` | `successful(command, flags)`, `forbidden(command)`, `existing_label(name)`, `readback(fields, values)`; `values`는 fixture의 의도한 최종 메타데이터 |
| `transcript` | `id`, `judge: manual`, `criterion`을 가진 의미·순서·독립성 판단 |

`checks`는 실행기가 호스트 종료 후 fixture에서 실행할 고정 `argv`와 제한 시간이다. 버그·미완성 구현 케이스는 원래 테스트 파일 보존과 실행기 테스트 결과를 함께 검사한다. 스냅샷은 `.git`, `.remote.git`, `.claude`, `__pycache__` 내부를 제외하며 일반 파일의 해시·모드, 심볼릭 링크 대상, 디렉터리와 Git 브랜치·HEAD·worktree를 기록한다. 파일 내용 보존은 중간 수정 여부를 증명하지 않으므로 리팩터링의 승인 전 수정 여부는 실행 순서도 검토한다.

`doc-edit`는 기존 `base` fixture를 사용한다. 고정 검사는 비어 있지 않은 docstring을 확인하고, 그 문자열의 행만 제거한 파일이 Git 기준 원문과 같은지 검사한다. 다른 추적 파일 변경과 새 비추적 파일도 허용하지 않는다. docstring의 의미는 수동으로 판단한다. 비문장 작업인 `bug-fix`, `refactor-approval`, `explain-code`, `general-review`, `architecture-review`, `implementation-finish`, `finish-cleanup`은 `humanizer` 선택도 금지한다.

`file_state`의 `requires: ["git_metadata_write"]`는 Git 메타데이터 쓰기를 전제로 하는 항목이다. 실행기는 호스트와 sandbox 정책에 따른 가능 여부와 이유를 `capabilities.git_metadata_write`에 기록한다. Codex의 `workspace-write`와 `read-only`는 `.git`을 읽기 전용으로 보호하므로 `finish-cleanup`의 작업 브랜치 삭제·worktree 등록 제거·worktree 경로 삭제는 이유와 함께 `not_applicable`로 보고한다. 지정 임시 파일 삭제와 사용자 파일·미병합 브랜치 보존, 기록 정비는 계속 검사한다. 호스트 안에서 쓰기 probe를 실행한 결과는 아니며, Claude도 개별 명령의 권한 거부가 발생할 수 있다. capability 기록이 없는 결과는 추정해서 제외하지 않고 `unknown`으로 남긴다.

채점은 선택, 참조 로딩, 기능 결과를 독립적으로 보고한다. 성공한 Skill dispatch 또는 반환된 SKILL 전체 본문이 선택의 증거다. 경로 언급이나 실패한 읽기는 성공한 선택으로 세지 않는다. 호출 ID와 결과를 연결하고, shell 전체가 성공해도 개별 파일의 읽기 오류를 확인한다. 원문과 일치하는 반환 범위를 먼저 판정하고, 그 밖의 출력에서 오류·권한 거부를 확인한다. 참조를 전부 출력한 뒤 다른 명령이 실패해도 해당 읽기는 `full`이다. 명령의 `head`/`limit`, 경로 존재 확인, 읽겠다는 설명만으로 통과시키지 않는다. 읽기 기록에는 `full`, `partial`, `failed`, `blocked`, `unknown`을 남긴다. 로딩은 지침 적용의 증거와 구분한다.

Humanizer 로딩 기록의 `load_source`는 파일 읽기의 `file_read` 또는 Claude 주입의 `skill_dispatch`다. dispatch 로딩은 `Skill`의 `humanizer` 호출, 성공한 `Launching skill: humanizer` 결과, 바로 다음 `isSynthetic: true` 사용자 메시지의 텍스트 블록을 연결해 판정한다. 블록은 `Base directory for this skill: <path>`와 빈 줄로 시작해야 한다. 실제 base 경로가 checkout의 `external/humanizer`와 같고, 주입 본문이 frontmatter를 제외한 원문 전체와 일치해야 한다. 실패·차단·다른 경로/namespace·부분 본문·연결되지 않은 본문은 로딩으로 세지 않는다. 호출 결과에 본문이 직접 들어 있다고 가정하지 않는다. `--self-check`는 이 stream-json 구조를 합성한 작은 fixture로 성공과 거부 조건을 검사하며 임시 파일은 자동 삭제한다.

PR 케이스의 수동 판정은 반환 산출물과 게시된 제목·본문에 Humanizer의 초안·패턴 목록·재작성 구조가 남지 않고 조건·부정·검증 한계를 보존하는지 확인한다. 각 실행의 필수 조건을 함께 만족한 결과만 집계하며, 파일 대체 케이스는 통과 기준에 합치지 않고 별도 보고한다.

호스트 없이 실행할 기본 검사는 다음과 같다. 모든 fixture 종류(`base`, `agents`, `bug`, `incomplete`, `pr`, `pr-open`, `finish`)를 각각 새 임시 경로에 생성하고, 부모 저장소와 서브모듈의 추적 파일 목록·로컬 링크도 확인한다. 이 검사는 실제 호스트의 선택률이나 문장 품질을 검증하지 않는다.

```bash
bash -n evals/run.sh evals/fixtures.sh
python3 -m py_compile evals/score.py evals/bin/gh
rm -r evals/__pycache__ evals/bin/__pycache__
python3 evals/score.py --self-check
```

각 assertion과 축의 결과는 `pass`, `fail`, `unknown`, `not_applicable`이다. 필수 읽기의 부분 로딩·잘못된 경로는 `fail`, 승인 차단·결과 누락은 `unknown`이다. 완전한 로그에서 필수 행동이 관측되지 않으면 실패다. 비선택 판정에는 누락 없는 로그가 필요하며 하위 에이전트 내부 도구가 수집되지 않으면 부재를 단정하지 않는다. 미지원 Codex 이벤트도 보고서에 표시하고 부재 판정의 증거로 쓰지 않는다. 검사할 항목이 없는 축은 `not_applicable`이다. 실패가 하나라도 있으면 해당 축과 전체는 실패, 실패 없이 미판정이 있으면 `unknown`이다.

의미 판단은 정규식으로 대신하지 않는다. `manual:` 항목은 자동 보고서에서 `unknown`으로 남는다. 검토자는 실제 반환 결과, 최종 산출물, 하위 에이전트 호출·완료·독립성 증거를 읽고 별도 결과 기록에 판정과 근거를 남긴다. 검수자 이름이나 spawn 호출 입력만으로 fresh review를 인정하지 않는다. legacy 모드에서 사라진 fixture나 하위 에이전트 증거를 성공으로 복원하지 않는다.

## 실행 경계

[bin/gh](bin/gh)는 호출 인자·작업 디렉터리·종료 코드·stdout/stderr·전후 PR 상태를 기록하는 로컬 stub이다. `auth status`, `repo view`, `label list`, `pr list/create/view/edit/ready/diff`의 제한된 계약을 제공한다. JSON 읽기 명령의 `--jq`/`-q`는 선택한 JSON을 로컬 `jq -r`에 전달한다. `--template`과 지원하지 않는 명령·JSON 필드는 실패한다. 채점기도 실제 필터 출력으로 라벨·readback을 검사한다. readback은 마지막 성공 쓰기 이후 성공한 `pr view`의 필드를 합쳐 최종 상태와 비교하며, 같은 필드는 마지막 반환값을 사용한다. 필수 필드가 모든 재조회에서 빠지면 실패다. `pr ready`도 상태를 바꾸고 기록하므로 금지 행동을 탐지할 수 있다. 실제 gh로 위임하거나 네트워크에 접속하지 않는다. PR 케이스는 이 stub 계약을 검증하며 실제 GitHub 연동을 검증하지 않는다.

`pr create`로 생성한 PR은 JSON 필드 `number`, `url`, `state`, `title`, `body`, `baseRefName`, `headRefName`, `isDraft`, `labels`, `files`, `commits`, `headRefOid`를 지원한다. 생성할 때와 edit로 base를 바꿀 때 로컬 Git에서 `base...head`의 파일 경로, `base..head`의 커밋 OID, head 커밋 OID를 계산한다. 유효하지 않은 ref나 Git 비교 오류가 있으면 호출을 실패로 기록하고 기존 PR 상태를 보존한다.

Git origin은 각 fixture 내부의 bare 저장소다. 실행 전에 로그인 shell의 `command -v gh`가 stub을 가리키고 origin의 fetch/push 주소가 모두 해당 로컬 경로인지 확인하며, 불일치하면 호스트를 실행하지 않는다. `PATH` 맨 앞에 `evals/bin`을 넣고 `ZDOTDIR`을 빈 디렉터리로 지정한다. 사용자 zsh 시작 파일이 PATH를 다시 정렬해 실제 gh를 선택하는 것을 피하기 위한 설정이다. 시스템 시작 파일이나 다른 shell 설정은 남으므로 사전 확인이 실패할 수 있다.

stub과 로컬 origin은 정상 `gh` 호출과 해당 origin의 Git 작업을 로컬로 돌린다. 절대경로의 실제 gh, curl·Python 등의 다른 네트워크 호출, 새 remote, 사용자 전역 설정·hook까지 차단하는 완전한 네트워크 격리는 아니다. Codex는 항상 `approval_policy="never"`와 케이스의 sandbox를 사용한다. 승인 거부는 통과 증거가 아니다. Claude는 지정한 도구 허용 목록과 호스트의 권한 검사를 사용한다. 더 강한 격리가 필요하면 외부 실행 환경에서 제공한다.
