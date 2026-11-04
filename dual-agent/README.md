# Dual Agent

서로 다른 두 AI 에이전트가 설계·구현·검수를 나눠 코드를 변경한다. 기본은 Claude가 문제 정의와 설계, 검수를 맡고 Codex가 구현을 맡는다. 코드를 쓴 모델과 승인하는 모델이 같지 않도록 작성자와 검수자를 분리한다.

명시적으로 호출할 때만 실행한다. 작업이 맞아 보여도 자동으로 선택되지 않는다. Claude Code(`/dual-agent`)와 Codex CLI(`$dual-agent`) 어느 쪽에서도 실행할 수 있다. 실행한 쪽이 호스트가 되어 자기 모델의 역할을 직접 맡고, 상대 모델은 CLI로 호출한다. Claude Code에서는 `codex exec`, Codex에서는 `claude -p`를 쓴다. 역할은 호스트와 상관없이 설정을 따른다.

```text
/dual-agent 결제 웹훅 재시도 로직을 추가해줘. 방향: 기존 이벤트 스키마는 유지
/dual-agent --mode codex-heavy 이 모듈을 리팩터링해줘.
$dual-agent --gates off 로그인 에러 메시지를 정리해줘.
```

## 흐름

1. **문제 정의 토론**(요구가 모호하거나 큰 작업): 주도자가 `problem.md`를 쓰고 상대 모델이 읽기 전용으로 비판한다. 요청에 드러난 증상에서 실제 원인을 찾아 정의한다.
2. **설계**: `design.md`를 확정하고 상대 모델이 비판한다.
3. **구현**: 작업자가 `design.md`대로 구현한다.
4. **검수·토의·재작업**: 반대편 모델이 diff를 수용 기준에 맞춰 검수하고, 지적을 `FIX`·`NO-CHANGE`·`OPEN`으로 나눈다. 이견은 토의하고 `FIX`만 다시 위임한다.
5. **마무리**: 요약과 검증 결과를 남기고 설정에 따라 커밋한다.

작업 산출물은 `.planning/dual-agent/<slug>/`에 파일로 남긴다. `.planning/`이 Git에서 무시되지 않으면 `*`만 담은 `.planning/.gitignore`를 만들어 산출물이 커밋되지 않게 한다. 라운드 상한을 넘기거나, 두 모델의 의견이 교착되거나, 상대 모델 호출이 실패하면 게이트 설정과 상관없이 멈추고 사용자에게 보고한다. 호출이 실패하면 사용자에게 묻기 전에는 혼자 작업하는 방식으로 바꾸지 않는다.

## 설정

저장소 루트의 `.dualagent.toml`로 역할 분담, 승인 게이트, 라운드 한도를 정한다. 파일이 없으면 첫 실행을 시작할 때 역할 분담과 게이트를 물어 `.dualagent.toml`로 저장한 뒤 진행한다. 저장하지 않겠다고 하면 기본값으로 진행한다. 우선순위는 이번 요청, 저장소 지침(`AGENTS.md` 등), `.dualagent.toml`, 기본값 순이다.

```toml
version = 1

[roles]
lead = "claude"        # claude | codex | user
worker = "codex"       # codex | claude | split
reviewer = "auto"      # auto = 작업자의 반대편 모델

[gates]                # ask = 승인 대기, auto = 요약 후 계속
problem = "ask"
design = "ask"
commit = "ask"         # ask | auto | never

[workflow]
problem_debate = "auto"   # auto | always | never
debate_rounds = 2
review_rounds = 3
worker_timeout_sec = 1800
```

| 설정 | 기본값 | 설명 |
|------|--------|------|
| `roles.lead` | `claude` | 문제 정의·설계 초안 작성자 |
| `roles.worker` | `codex` | 구현 담당. `split`은 설계 판단이 핵심인 부분만 Claude가 맡는다 |
| `roles.reviewer` | `auto` | 작업자의 반대편 모델 |
| `gates.problem` | `ask` | 문제 정의 합의 후 승인 |
| `gates.design` | `ask` | 설계 확정 후, 구현 전 승인 |
| `gates.commit` | `ask` | 검수 통과 후 커밋 방식 |

`ask`는 승인을 기다리고 `auto`는 요약을 보여 준 뒤 계속한다. `auto`도 검증과 검수는 건너뛰지 않는다. 푸시와 PR은 어떤 설정에서도 따로 요청해야 한다.

프로필이 있어도 설정을 바꾸고 싶으면 직접 요청할 수 있다.

```text
/dual-agent 설정해줘. 설계 승인은 ask, 커밋은 never로 저장해줘.
```

## 호출 옵션

옵션은 이번 작업에만 적용되고 프로필을 바꾸지 않는다. "앞으로도"처럼 계속 쓰겠다고 하면 프로필에 저장할지 묻는다.

| 옵션 | 효과 |
|------|------|
| `방향: <지시>` (`direction:`도 가능) | 방향·제약·선호를 문제 정의에 그대로 기록하고 모든 단계의 기준으로 쓴다 |
| `--lead` `--worker` `--reviewer` | 역할 덮어쓰기 |
| `--gates on\|off\|<목록>` | 게이트 전부 켜기, 끄기, 일부만 켜기 |
| `--commit ask\|auto\|never` | 커밋 방식 |
| `--rounds <토론>,<검수>` | 라운드 상한 |
| `--debate always\|never` | 문제 정의 토론 강제·생략 |
| `--phase <단계>` | `problem`, `design`, `implement`, `review` 중 한 단계만 실행하고 그 단계 후 멈춘다 |
| `--mode <프리셋>` | `default`, `codex-heavy`, `claude-heavy`, `autopilot`, `careful` |

진행 중에도 게이트에서 승인 대신 새 방향을 줄 수 있다. 영향받는 이후 단계는 다시 수행한다.

## 사전 조건

Claude Code와 Codex CLI가 모두 설치되고 로그인되어 있어야 한다. `timeout` 또는 `gtimeout`도 필요하다(macOS 기본 설치에는 없다). 상대 모델 호출은 비대화형으로 실행한다. Codex에서 실행하면 `claude -p` 호출에 네트워크와 로그인 정보가 필요하므로, 호출할 때마다 샌드박스 밖 실행 승인을 요청한다. 설정과 해석 규칙은 [SKILL.md](SKILL.md)와 [프로필 참조](references/profile.md)를 따른다.

설치는 [저장소 안내](https://github.com/Yon-Fandorin/skills#설치)를 따른다. 실행할 쪽의 스킬 경로에 연결한다. Codex는 `~/.agents/skills`, Claude Code는 [Claude Code 안내](https://github.com/Yon-Fandorin/skills#claude-code)를 따른다.
