# UnitConverter 실습 회고 보고서

- **작성일**: 2026-06-05
- **프로젝트**: UnitConverter_29
- **이번 Export 세션**: `fcb065f8-a046-4234-8d2f-a8199870c9de` → [`Prompting/002-ecb-harness-rules-alignment.md`](../Prompting/002-ecb-harness-rules-alignment.md)
- **Prompting 누적**: 2개 (`001`, `002`)

---

## 1. 실습 목표와 달성도

| 목표 (README Activities) | 달성 | 근거 |
|--------------------------|------|------|
| 1. 문제 코드·요구사항 분석 | ✅ | [`Report/001`](../Report/001-UnitConverter_ProblemDefinition_Report.md), [`docs/PRD.md`](../docs/PRD.md), [`Prompting/001`](../Prompting/001-mom-test-문제정의-prd.md) 완료 |
| 2. OCP/SRP 기본 구현 | 🔄 | ECB Harness(`src/entity|control|boundary`)·`.cursorrules` 정렬 완료, **구현 코드 미작성** |
| 3. TC 구현 | ❌ | `tests/` 디렉터리 골격만 존재, Test ID별 RED 스켈레톤 없음 |
| 4. 추가 요구사항 (EXT) | ❌ | EXT-01~03 미착수 |
| 5. 회고 및 발표 | 🔄 | 본 보고서·Prompting Export (진행 중) |

---

## 2. AI 활용 — 도움이 된 순간과 한계

| 순번 | Prompting | 활용 | 도움이 된 점 | 한계 |
|------|-----------|------|-------------|------|
| 001 | [001-mom-test-문제정의-prd](Prompting/001-mom-test-문제정의-prd.md) | Ask · Agent | Mom Test·R-G-I-O·PRD 초안·문서 SSOT 연결 | 솔루션 섞임 방지는 사용자 검수 필요 |
| 002 | [002-ecb-harness-rules-alignment](Prompting/002-ecb-harness-rules-alignment.md) | Agent · Ask(리뷰) | ECB Harness 일괄 생성, `.cursorrules` 갭 리뷰·SSOT 정렬 | 초안 미첨부 시 Rule 문장 단위 리뷰 불가; Hook은 원칙만 기록 |

**이번 세션 핵심 산출**

- `pyproject.toml` + `src/`·`tests/` ECB 골격
- `.cursorrules` 헌법 개편 (E001~E007, import 방향, TDD 게이트)
- Skill·Command·reference·PRD ECB 경로 통일

---

## 3. TDD·테스트 (Dual-Track)

**pytest 결과** (2026-06-05):

```text
python -m pytest tests/ -v
→ collected 0 items (Harness만 존재, exit code 5)
```

| Phase | Test ID | 상태 |
|-------|---------|------|
| RED | D-CNV-01 ~ D-CFG-01 | 미작성 |
| RED | U-IN-01 ~ U-OUT-01 | 미작성 |
| GREEN / REFACTOR | — | 해당 없음 |

**TC 작성 팁** (Transcript·설계 기준)

- Track B(Logic)는 `tests/entity/`·`tests/control/` — entity/control Mock 금지
- Track A(UI)는 `tests/boundary/` — E00x stderr 계약을 Then에 명시
- RED는 `pytest.fail("RED: [Test ID]")` 한 줄로 의도적 FAIL 확인 후 GREEN

---

## 4. 클린코드·리팩토링

| 항목 | 상태 |
|------|------|
| ECB import (`boundary → control → entity`) | `.cursorrules`·`reference.md`에 SSOT화 |
| OCP/SRP | Registry 확장·레이어 분리 원칙 문서화, 코드 미구현 |
| `/refactor-smell`, `/refactor-safe` | 미사용 (테스트 PASS 전제 미충족) |

**장점**: Harness·Rule·Skill 정렬로 RED부터 Layer·Track 혼선 감소 기대  
**어려움**: legacy `unit_converter/` 설명과 ECB 전환 구간에서 문서·Command 동시 갱신 필요

---

## 5. 다음 단계

1. **RED** — `D-CNV-01`부터 `/red-test-plan` → `/red-skeleton` (`tests/entity/`)
2. **GREEN** — `/green-minimal`로 `src/entity/` 최소 구현
3. **UI Track** — U-IN-01~03 + E001~E003 (`tests/boundary/`)
4. **Hook** — Golden Master·RED `src/**` 편집 차단 (`.cursor/hooks.json`)
5. **EXT** — P0 FR/NFR GREEN 후 `new_features` 브랜치에서 EXT-01~03

---

## 참고 문서

| 문서 | 용도 |
|------|------|
| [`.cursorrules`](../.cursorrules) | 헌법 · ECB · E00x · TDD 게이트 |
| [`reference.md`](../.cursor/skills/unit-converter-tdd/reference.md) | Test ID · C2C |
| [`Report/001`](../Report/001-UnitConverter_ProblemDefinition_Report.md) | 문제 정의 |
