# UnitConverter 실습 회고 보고서

- **작성일**: 2026-06-05
- **프로젝트**: UnitConverter_29
- **이번 Export 세션**: [`Prompting/013-refactor-safe-entity-registry-fixture-prompt.md`](../Prompting/013-refactor-safe-entity-registry-fixture-prompt.md)
- **Report 짝**: `Report/013-refactor-safe-entity-registry-fixture-report.md`
- **Prompting 누적**: 13개 (`001` … `013`)

---

## 1. 실습 목표와 달성도

| 목표 (README Activities) | 달성 | 근거 |
|--------------------------|------|------|
| 1. 문제 코드·요구사항 분석 | ✅ | [`Report/001`](../Report/001-UnitConverter_ProblemDefinition_Report.md), [`011`](../Report/011-refactor-smell-scan-report.md) P1 smell 식별 |
| 2. OCP/SRP 기본 구현 | 🔄 | entity OCP 충족 · control `ConvertUseCase` 스켈레톤([`012`](../Report/012-refactor-safe-control-layer-report.md)) |
| 3. TC 구현 | 🔄 | 4건 PASS + Golden Master · U-IN-03, U-OUT-01 미착수 |
| 4. 추가 요구사항 (EXT) | ❌ | EXT-01~03 미착수 |
| 5. 회고 및 발표 | 🔄 | 본 보고서·[`013-refactor-safe-entity-registry-fixture-prompt`](../Prompting/013-refactor-safe-entity-registry-fixture-prompt.md) |

**이번 세션 산출**

- **REFACTOR** (`/refactor-safe`) — P1 smell 1건: entity Registry 셋업 중복 제거
- `tests/entity/conftest.py` — `meter_feet_registry` fixture 추출
- D-CNV-01/02 Given 4줄 → fixture 1줄로 교체
- `src/**` **미수정** · 변환값·pytest.approx·Golden 계약 유지

---

## 2. AI 활용 — 도움이 된 순간과 한계

| 순번 | Prompting | 활용 Command/Skill | 도움이 된 점 | 한계 |
|------|-----------|-------------------|-------------|------|
| 001~012 | [001](../Prompting/001-mom-test-문제정의-prd.md) … [012](../Prompting/012-refactor-safe-control-layer-prompt.md) | RED/GREEN/REFACTOR | Dual-Track·Golden·control 추출 | — |
| **013** | [013-refactor-safe-entity-registry-fixture-prompt](../Prompting/013-refactor-safe-entity-registry-fixture-prompt.md) | `/refactor-safe` | 011 P1 후보를 tests-only Budget 내 1 fixture로 해소 | boundary subprocess 중복은 미처리 |

**이번 세션 핵심 인사이트**

- Logic Track 테스트에서 Registry 셋업은 **Given 공통 전제** — conftest fixture가 SSOT
- fixture가 `Converter`를 반환하면 테스트 본문은 When/Then에만 집중 — AAA 가독성 향상
- REFACTOR는 `tests/`만 수정해도 동일 Budget·계약 원칙 적용 — src 변경 없이 smell 제거 가능

---

## 3. TDD·테스트 (Dual-Track)

**pytest 결과** (2026-06-05):

```text
python -m pytest tests/ -v
→ collected 4 items → 4 passed

python -m pytest tests/entity/test_d_cnv_01.py tests/entity/test_d_cnv_02.py -v
→ 2 passed — Golden matched (UPDATE_GOLDEN 없음)
```

| Phase | Test ID | Track · Layer | 상태 |
|-------|---------|---------------|------|
| GREEN + Golden | U-IN-01, U-IN-02 | UI · boundary | ✅ PASS |
| GREEN + Golden | D-CNV-01, D-CNV-02 | Logic · entity | ✅ PASS |
| **REFACTOR** | — | entity fixture 중복 제거 | ✅ 완료 |
| RED | U-IN-03, U-OUT-01 | UI · boundary | ❌ 미착수 |
| RED | D-CNV-03, D-REG-01, D-CFG-01 | Logic | ❌ 미착수 |

**TC 작성 팁**

- `meter_feet_registry`는 meter+feet 등록 후 `Converter` 반환 — D-REG-01(동적 등록) RED 시 별도 fixture 추가 권장
- entity conftest는 `tests/conftest.py`(PYTHONPATH)와 분리 — 레이어별 fixture SSOT

---

## 4. 클린코드·리팩토링

### OCP/SRP 적용 경험

| 영역 | 상태 | 비고 |
|------|------|------|
| entity (NFR-01) | ✅ | REFACTOR 범위 외 — 미수정 |
| tests/entity | 🔄 | Registry 셋업 DRY — `conftest.py` fixture |
| control (NFR-02) | 🔄 | [`012`](../Report/012-refactor-safe-control-layer-report.md) 스켈레톤 유지 |
| boundary | 🔄 | subprocess Golden 유지 — P1 boundary fixture 중복 잔존 |

### `/refactor-safe` 사용

- **대상**: P1 entity Registry 셋업 중복 (011 스캔 2순위)
- **Budget**: 파일 3 · 클래스 0 · fixture 1 (`meter_feet_registry`)
- **변경 파일**: `tests/entity/conftest.py` (신규), `tests/entity/test_d_cnv_01.py`, `tests/entity/test_d_cnv_02.py`

---

## 5. 다음 단계

| 우선순위 | 작업 | Command |
|----------|------|---------|
| 1 | U-IN-03 (E003), U-OUT-01 (FR-02 출력) — UseCase에 변환·출력 연동 | `/green-minimal` |
| 2 | P1: boundary subprocess fixture 중복 제거 | `/refactor-safe` |
| 3 | D-CNV-03, D-REG-01, D-CFG-01 | RED/GREEN |
| 4 | EXT-01~03 | RED부터 |
