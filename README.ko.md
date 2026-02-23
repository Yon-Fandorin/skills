[English](README.md)

# Claude Code Agents

Claude Code에서 전역으로 사용할 수 있는 서브 에이전트(skills) 모음입니다.

각 에이전트는 독립된 디렉토리로 관리되며, `~/.claude/skills/`에 심볼릭 링크를 생성하여 모든 프로젝트에서 사용할 수 있습니다.

## 설치

```bash
git clone <repo-url> ~/project/claude-code-agents
cd ~/project/claude-code-agents
./install.sh install
```

Claude Code를 재시작하면 에이전트들이 자동으로 인식됩니다.

## 제거

```bash
cd ~/project/claude-code-agents
./install.sh uninstall
```

## 에이전트 목록

| 에이전트 | 명령어 | 설명 |
|---------|--------|------|
| Svelte 5 | `/svelte5` | Svelte 5 runes 문법, SvelteKit 패턴, 컴포넌트 생성, 코드 리뷰, 디버깅 |
| Rust Axum Backend | `/rust-axum-backend` | Axum 0.8.x API 라우팅, 핸들러/추출기 패턴, serde 직렬화, 요청 검증, utoipa OpenAPI 문서화, 에러 처리, 프로젝트 구조 |
| Rust Style | `/rust-style` | 프레임워크 무관 Rust 스타일 컨벤션 — use 정렬, 모듈 구조, 네이밍, 에러 설계, 문서화, 관용 패턴 |

## 에이전트 추가 방법

1. 새 디렉토리 생성 (예: `react/`)
2. `SKILL.md` 작성 (frontmatter + 프롬프트)
3. 필요한 레퍼런스 파일 추가
4. `./install.sh install` 재실행

## 사용 예시

```
/svelte5 Counter 컴포넌트 만들어줘
/svelte5 이 코드 리뷰해줘
/svelte5 $effect 사용법 알려줘

/rust-axum-backend CRUD API 핸들러 만들어줘
/rust-axum-backend 프로젝트 구조 잡아줘
/rust-axum-backend OpenAPI 문서화 추가해줘

/rust-style 이 파일 스타일 리뷰해줘
/rust-style src/ 디렉토리 import 정리해줘
/rust-style rustfmt, Clippy 설정 잡아줘
```
