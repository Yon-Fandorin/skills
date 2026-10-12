# Codewright

저장소 규칙에 맞춰 코드를 작성·리팩터링하거나 변경을 검토한다.

```text
$codewright로 이 변경을 구현해줘.
$codewright로 현재 변경의 코드 배치와 가독성을 검토해줘.
```

검토만 요청하면 파일을 수정하지 않는다. 실행 규칙과 언어·프레임워크별 참조는 [SKILL.md](SKILL.md), 언어·배치 승인 설정은 [저장소 프로필](references/repository-language-profile.md)을 따른다.

설치는 [저장소 안내](../README.md#설치)를 참고한다.

## 처음 사용하기

구현 작업에서 저장소 루트에 `.codewright.toml`이 없으면 언어와 코드 배치 승인 방식을 함께 설정하도록 안내한다. 설정을 건너뛰어도 기존 저장소 규칙과 기본값으로 작업을 계속한다. 검토만 요청한 경우에는 설정을 묻거나 파일을 만들지 않는다.

```text
$codewright 설정해줘. 주석·API 문서·테스트 설명은 한국어, 배치 승인은 auto로 저장해줘.
README와 일반 문서는 한국어, 에이전트용 지침은 영어로 AGENTS.md에 기록해줘.
```

| 설정 | 적용 대상 | 기본값 |
|------|-----------|--------|
| `language.comments` | 코드 주석 | `en` |
| `language.api_documentation` | Rustdoc·Docstring 같은 코드 API 문서 | `en` |
| `language.test_descriptions` | 테스트 시나리오·예상 결과 설명 | `en` |
| `approval.shape` | 새 디렉터리·모듈·테스트 계층의 배치 승인 | `ask` |

`ask`는 제안한 배치가 아직 승인되지 않았으면 승인을 기다린다. `auto`는 작업 범위와 소유자가 정해진 배치를 설명한 뒤 계속한다. 기존에 승인된 계층을 일관되게 확장하면서 공유 범위를 넓히지 않는 경우에는 `ask`도 다시 묻지 않는다. 두 모드 모두 검증과 리뷰를 수행하며, 별도 소유자 결정이나 도구 실행 권한을 대신하지 않는다.

이미 정해진 저장소 규칙이 있으면 그 규칙을 우선한다. README·일반 문서와 에이전트용 Markdown 지침의 언어는 원할 때 `AGENTS.md`에 별도로 기록한다. `.codewright.toml`은 이 문서들의 언어를 지정하지 않는다.
