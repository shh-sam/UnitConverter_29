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
| 3. TC 구현 | 🔄 | **RED 설계표만** 완료(D-LOC-01, U-IN-01~02) — 스켈레톤·pytest FAIL **미착수** |
| 4. 추가 요구사항 (EXT) | ❌ | EXT-01~03 미착수 |
| 5. 회고 및 발표 | 🔄 | 본 보고서·Prompting Export (진행 중) |

**이번 세션 산출**

- `/red-test-plan` — Logic Track **D-LOC-01** RED 설계표 (C2C·테스트 플랜·ECB 점검)
- `/red-test-plan` — UI Track **U-IN-01, U-IN-02** RED 설계표 (E001/E002 계약)
- Magic Square vs UnitConverter SSOT 혼선 정정 (`grid=None→E003` → UnitConverter `""→E001`)

---

## 2. AI 활용 — 도움이 된 순간과 한계

| 순번 | Prompting | 활용 Command/Skill | 도움이 된 점 | 한점 |
|------|-----------|-------------------|-------------|------|
| 001 | [001-mom-test-문제정의-prd](../Prompting/001-mom-test-문제정의-prd.md) | Ask | Mom Test·PRD·문서 SSOT | — |
| 002 | [002-ecb-harness-rules-alignment](../Prompting/002-ecb-harness-rules-alignment.md) | Agent | ECB Harness·`.cursorrules` 정렬 | Hook 미구현 |
| **003** | [003-dual-track-red-test-plan-prompt](../Prompting/003-dual-track-red-test-plan-prompt.md) | `/red-test-plan` (Ask) | Dual-Track RED 표·C2C Rule 1~3·Expected RED Failure·PRD 갭 명시 | FR-LOC-01 PRD 미등록 — 워크북 의존 |

**이번 세션 핵심 인사이트**

- `docs/PRD.md`에 FR-LOC-01 없음 → C2C 설계 시 **SSOT 갭을 명시**하고 워크북/MagicSquare 참조로 보완
- 실습자가 Magic Square 용어(`grid`, `E003`)를 UnitConverter U-IN에 혼용 → **reference.md 기준으로 즉시 정정** 필요
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
| RED 설계 | D-LOC-01 (FR-LOC-01) | Logic · entity | ✅ 설계표 완료 — 스켈레톤·FAIL 미작성 |
| RED 설계 | U-IN-01, U-IN-02 | UI · boundary | ✅ 설계표 완료 — 스켈레톤·FAIL 미작성 |
| RED | D-CNV-01 ~ D-CFG-01 | Logic | ❌ 미착수 |
| RED | U-IN-03, U-OUT-01 | UI | ❌ 미착수 |
| GREEN / REFACTOR | — | — | 해당 없음 |

**TC 작성 팁** (Transcript·설계 기준)

- Logic Track RED: `pytest.fail` 한 줄 + `find_blank_coords` 실제 import — Domain Mock 금지
- UI Track RED: `subprocess`/`capsys`로 `python -m boundary ""` — stderr `E001`/`E002` 계약을 Then에 명시
- Magic Square 워크북 ID(D-LOC-*)와 UnitConverter P0 ID(D-CNV-*) **혼용 주의** — `reference.md` SSOT 우선
- PRD에 없는 FR-LOC-01은 설계 전 PRD·reference 동기화 권장

---

## 4. 클린코드·리팩토링

| 항목 | 상태 |
|------|------|
| ECB import (`boundary → control → entity`) | `.cursorrules`·`reference.md` SSOT — 코드 미구현 |
| OCP/SRP | RED 설계표에서 PASS 판정, 구현 없음 |
| `/refactor-smell`, `/refactor-safe` | 미사용 (테스트 PASS 전제 미충족) |

**장점**: Ask 모드 RED 설계로 Layer·Track·Mock 규칙을 코드 작성 전에 고정  
**어려움**: 워크북(Magic Square) 용어와 UnitConverter PRD 불일치 — 실습자·Agent 모두 SSOT 확인 비용

---

## 5. 다음 단계

1. **PRD 동기화** — FR-LOC-01 제거 또는 UnitConverter 도메인에 맞는 FR/Test ID로 정리 (D-CNV-01부터 권장)
2. **RED 스켈레톤** — `/red-skeleton`으로 `D-CNV-01` 또는 설계 확정 ID부터 `tests/entity/`·`tests/boundary/`
3. **GREEN** — `/green-minimal`로 `src/entity/` 또는 `src/boundary/` 최소 구현
4. **UI Track** — U-IN-01~03 + E001~E003 (`tests/boundary/`)
5. **Hook** — Golden Master·RED `src/**` 편집 차단 (`.cursor/hooks.json`)
