# Skill Reviewer

프레시 컨텍스트 에이전트가 AI Hero 작성 지침과 대상 유형에 맞는 스킬 원문을 읽고, 호출 조건·지침 구조·참조 연결·완료 기준을 검토한다.

```text
$skill-reviewer로 이 스킬의 지침과 참조 구조를 검토해줘.
```

기본은 읽기 전용이다. 지적 사항과 검토 근거를 제시하고 `Ready` 또는 `Revisions required`를 판정한다. 독립 검수나 필수 원문 확인을 완료하지 못하면 `Review incomplete`로 표시한다.

검토 기준과 보고 형식은 [SKILL.md](SKILL.md), 설치는 [저장소 안내](../README.md#설치)를 참고한다.
