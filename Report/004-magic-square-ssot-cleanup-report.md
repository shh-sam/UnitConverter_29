# UnitConverter 실습 회고 보고서

- **작성일**: 2026-06-05
- **프로젝트**: UnitConverter_29
- **이번 Export 세션**: `16a1094f-3258-49f2-86a2-2c3d4fa473fe` → [`Prompting/004-magic-square-ssot-cleanup-prompt.md`](../Prompting/004-magic-square-ssot-cleanup-prompt.md)
- **Report 짝**: `Report/004-magic-square-ssot-cleanup-report.md`
- **Prompting 누적**: 4개 (`001`, `002`, `003`, `004`)

---

## 1. 실습 목표와 달성도

| 목표 (README Activities) | 달성 | 근거 |
|--------------------------|------|------|
| 1. 문제 코드·요구사항 분석 | ✅ | [`Report/001`](../Report/001-UnitConverter_ProblemDefinition_Report.md), [`docs/PRD.md`](../docs/PRD.md) — 선행 완료 |
| 2. OCP/SRP 기본 구현 | 🔄 | ECB Harness(`src/entity|control|boundary`)만 존재, **구현 코드 미작성** |
| 3. TC 구현 | 🔄 | RED 설계표(D-CNV-01, U-IN-01~02) 완료 — **스켈레톤·pytest FAIL 미착수** |
| 4. 추가 요구사항 (EXT) | ❌ | EXT-01~03 미착수 |
| 5. 회고 및 발표 | 🔄 | 본 보고서·Prompting Export (진행 중) |

**이번 세션 산출**

- Magic Square 잔존 용어 **전수 조사** — `Prompting/003`, `Report/003`, README, pytest 캐시
- UnitConverter SSOT(`reference.md`) 기준으로 **003 문서 일괄 정리** (D-CNV-01, U-IN-01~02)
- Magic Square conftest **pytest 캐시 삭제**

---

## 2. AI 활용 — 도움이 된 순간과 한계

| 순번 | Prompting | 활용 Command/Skill | 도움이 된 점 | 한계 |
|------|-----------|-------------------|-------------|------|
| 001 | [001-mom-test-문제정의-prd](../Prompting/001-mom-test-문제정의-prd.md) | Ask | Mom Test·PRD·문서 SSOT | — |
| 002 | [002-ecb-harness-rules-alignment](../Prompting/002-ecb-harness-rules-alignment.md) | Agent | ECB Harness·`.cursorrules` 정렬 | Hook 미구현 |
| 003 | [003-dual-track-red-test-plan-prompt](../Prompting/003-dual-track-red-test-plan-prompt.md) | `/red-test-plan` | Dual-Track RED 설계표 | — |
| **004** | [004-magic-square-ssot-cleanup-prompt](../Prompting/004-magic-square-ssot-cleanup-prompt.md) | Ask + Agent | SSOT 혼입 탐지·문서 일괄 정리 | 003 Export 당시 워크북 용어 혼입 — 사후 수정 필요 |

**이번 세션 핵심 인사이트**

- 실습 워크북(Magic Square) Test ID·도메인 용어가 Export 문서에 섞이면 **후속 RED/TDD 전체가 오염**됨
- `reference.md`·`docs/PRD.md`를 SSOT로 두고, Export·Prompting 작성 시 **도메인 ID 교차 검증** 필요
- 삭제된 테스트 소스보다 `__pycache__` 캐시가 혼란을 유발 — 정리 시 캐시도 함께 확인

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

**저장소 상태** (Export 시점)

- `src/entity|control|boundary/` — `__init__.py`만 존재
- `tests/entity|control|boundary/` — `__init__.py`만 존재
- `.md`/`.py`에서 Magic Square·D-LOC-* 문자열 **0건** (정리 완료)

**TC 작성 팁**

- Export·Prompting 문서도 **코드와 동일 SSOT**(`reference.md`)로 검증할 것
- Logic Track RED는 `Converter.convert` 등 **실제 import** + `pytest.fail` — Domain Mock 금지
- UI Track RED는 `""→E001`, `meter→E002` 계약을 Then에 명시

---

## 4. 클린코드·리팩토링

| 항목 | 상태 |
|------|------|
| ECB import (`boundary → control → entity`) | SSOT 정의됨 — 코드 미구현 |
| OCP/SRP | 문서·설계 단계, 구현 없음 |
| `/refactor-smell`, `/refactor-safe` | 미사용 (테스트 PASS 전제 미충족) |

**장점**: SSOT 불일치를 조기에 발견하고 Export 문서까지 일괄 정리  
**어려움**: 워크북·UnitConverter ID 혼용은 RED 설계 단계에서 차단하지 않으면 Export·README까지 전파됨

---

## 5. 다음 단계

1. **RED 스켈레톤** — `/red-skeleton`으로 `D-CNV-01`부터 `tests/entity/`
2. **UI Track RED** — U-IN-01~02 `tests/boundary/`
3. **GREEN** — `/green-minimal`로 `src/entity/` 또는 `src/boundary/` 최소 구현
4. **Logic Track** — D-CNV-02~03, D-REG-01, D-CFG-01 순차 RED
5. **Hook** — RED Phase `src/**` 편집 차단 (`.cursor/hooks.json`)
