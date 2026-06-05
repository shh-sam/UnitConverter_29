# UnitConverter 실습 회고 보고서

- **작성일**: 2026-06-05
- **프로젝트**: UnitConverter_29
- **이번 Export 세션**: `bd502df9-e85c-4aff-bd58-cb813f589239` → [`Prompting/003-dual-track-red-test-plan-prompt.md`](../Prompting/003-dual-track-red-test-plan-prompt.md)
- **Report 짝**: `Report/003-dual-track-red-test-plan-report.md`
- **Prompting 누적**: 3개 (`001`, `002`, `003`)

---

## 1. 실습 목표와 달성도

| 목표 (README Activities) | 달성 | 근거 |
|--------------------------|------|------|
| 1. 문제 코드·요구사항 분석 | ✅ | [`Report/001`](../Report/001-UnitConverter_ProblemDefinition_Report.md), [`docs/PRD.md`](../docs/PRD.md) — 선행 완료 |
| 2. OCP/SRP 기본 구현 | 🔄 | ECB Harness(`src/entity|control|boundary`)만 존재, **구현 코드 미작성** |
| 3. TC 구현 | 🔄 | **RED 설계표만** 완료(D-CNV-01, U-IN-01~02) — 스켈레톤·pytest FAIL **미착수** |
| 4. 추가 요구사항 (EXT) | ❌ | EXT-01~03 미착수 |
| 5. 회고 및 발표 | 🔄 | 본 보고서·Prompting Export (진행 중) |

**이번 세션 산출**

- `/red-test-plan` — Logic Track **D-CNV-01** RED 설계표 (C2C·테스트 플랜·ECB 점검)
- `/red-test-plan` — UI Track **U-IN-01, U-IN-02** RED 설계표 (E001/E002 계약)

---

## 2. AI 활용 — 도움이 된 순간과 한계

| 순번 | Prompting | 활용 Command/Skill | 도움이 된 점 | 한점 |
|------|-----------|-------------------|-------------|------|
| 001 | [001-mom-test-문제정의-prd](../Prompting/001-mom-test-문제정의-prd.md) | Ask | Mom Test·PRD·문서 SSOT | — |
| 002 | [002-ecb-harness-rules-alignment](../Prompting/002-ecb-harness-rules-alignment.md) | Agent | ECB Harness·`.cursorrules` 정렬 | Hook 미구현 |
| **003** | [003-dual-track-red-test-plan-prompt](../Prompting/003-dual-track-red-test-plan-prompt.md) | `/red-test-plan` (Ask) | Dual-Track RED 표·C2C Rule 1~3·Expected RED Failure | — |

**이번 세션 핵심 인사이트**

- `docs/PRD.md`·`reference.md`를 SSOT로 C2C 추적 — FR-02 → D-CNV-01, FR-05 → U-IN-01~02
- RED 설계(Ask)와 RED 스켈레톤(Agent) Phase 분리가 Command로 잘 고정됨

---

## 3. TDD·테스트 (Dual-Track)

**pytest 결과** (2026-06-05):

```text
python -m pytest tests/ -v
→ collected 0 items (Harness만 존재, exit code 5)
```

| Phase | Test ID | Track | 상태 |
|-------|---------|-------|------|
| RED 설계 | D-CNV-01 (FR-02) | Logic · entity | ✅ 설계표 완료 — 스켈레톤·FAIL 미작성 |
| RED 설계 | U-IN-01, U-IN-02 | UI · boundary | ✅ 설계표 완료 — 스켈레톤·FAIL 미작성 |
| RED | D-CNV-02 ~ D-CFG-01 | Logic | ❌ 미착수 |
| RED | U-IN-03, U-OUT-01 | UI | ❌ 미착수 |
| GREEN / REFACTOR | — | — | 해당 없음 |

**TC 작성 팁** (Transcript·설계 기준)

- Logic Track RED: `pytest.fail` 한 줄 + `Converter.convert` 실제 import — Domain Mock 금지
- UI Track RED: `subprocess`/`capsys`로 `python -m boundary ""` — stderr `E001`/`E002` 계약을 Then에 명시
- Test ID·오류 코드는 `reference.md` SSOT 우선

---

## 4. 클린코드·리팩토링

| 항목 | 상태 |
|------|------|
| ECB import (`boundary → control → entity`) | `.cursorrules`·`reference.md` SSOT — 코드 미구현 |
| OCP/SRP | RED 설계표에서 PASS 판정, 구현 없음 |
| `/refactor-smell`, `/refactor-safe` | 미사용 (테스트 PASS 전제 미충족) |

**장점**: Ask 모드 RED 설계로 Layer·Track·Mock 규칙을 코드 작성 전에 고정

---

## 5. 다음 단계

1. **RED 스켈레톤** — `/red-skeleton`으로 `D-CNV-01`부터 `tests/entity/`·`tests/boundary/`
2. **GREEN** — `/green-minimal`로 `src/entity/` 또는 `src/boundary/` 최소 구현
3. **UI Track** — U-IN-01~03 + E001~E003 (`tests/boundary/`)
4. **Logic Track** — D-CNV-02~03, D-REG-01, D-CFG-01 순차 RED
5. **Hook** — Golden Master·RED `src/**` 편집 차단 (`.cursor/hooks.json`)
