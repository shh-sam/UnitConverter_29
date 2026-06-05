# UnitConverter 실습 회고 보고서

- **작성일**: 2026-06-05
- **프로젝트**: UnitConverter_29
- **이번 Export 세션**: `038161a9-bd77-4b56-97cb-1a979e3ed47f` → [`Prompting/007-green-minimal-d-cnv-02-prompt.md`](../Prompting/007-green-minimal-d-cnv-02-prompt.md)
- **Report 짝**: `Report/007-green-minimal-d-cnv-02-report.md`
- **Prompting 누적**: 7개 (`001` … `007`)

---

## 1. 실습 목표와 달성도

| 목표 (README Activities) | 달성 | 근거 |
|--------------------------|------|------|
| 1. 문제 코드·요구사항 분석 | ✅ | [`Report/001`](../Report/001-UnitConverter_ProblemDefinition_Report.md), [`docs/PRD.md`](../docs/PRD.md) |
| 2. OCP/SRP 기본 구현 | 🔄 | `src/entity/` 4모듈 유지 · D-CNV-02 GREEN 시 **Converter 본문 미수정** (NFR-01) |
| 3. TC 구현 | 🔄 | D-CNV-01~02 **GREEN PASS** · U-IN-01~02 **RED** 유지 |
| 4. 추가 요구사항 (EXT) | ❌ | EXT-01~03 미착수 |
| 5. 회고 및 발표 | 🔄 | 본 보고서·[`007-green-minimal-d-cnv-02-prompt`](../Prompting/007-green-minimal-d-cnv-02-prompt.md) |

**이번 세션 산출**

- `/green-minimal` 재실행 — D-CNV-01은 006 세션에서 이미 GREEN, 추가 변경 없음 확인
- **D-CNV-02** GREEN — `tests/entity/test_d_cnv_02.py` 신규 (`2.5 m → 8.20210 feet`, FR-02)
- `src/` 변경 없음 — registry 기반 `Converter`가 meter→feet 변환을 이미 처리 (OCP 검증)

---

## 2. AI 활용 — 도움이 된 순간과 한계

| 순번 | Prompting | 활용 Command/Skill | 도움이 된 점 | 한계 |
|------|-----------|-------------------|-------------|------|
| 001 | [001-mom-test-문제정의-prd](../Prompting/001-mom-test-문제정의-prd.md) | Ask | Mom Test·PRD SSOT | — |
| 002 | [002-ecb-harness-rules-alignment](../Prompting/002-ecb-harness-rules-alignment.md) | Agent | ECB Harness·`.cursorrules` | Hook 미구현 |
| 003 | [003-dual-track-red-test-plan-prompt](../Prompting/003-dual-track-red-test-plan-prompt.md) | `/red-test-plan` | RED 설계표·C2C | — |
| 004 | [004-magic-square-ssot-cleanup-prompt](../Prompting/004-magic-square-ssot-cleanup-prompt.md) | `/session-export` | SSOT 혼입 정리 | — |
| 005 | [005-dual-track-red-skeleton-prompt](../Prompting/005-dual-track-red-skeleton-prompt.md) | `/red-skeleton` | RED 스켈레톤 3건 | — |
| 006 | [006-green-minimal-d-cnv-01-prompt](../Prompting/006-green-minimal-d-cnv-01-prompt.md) | `/green-minimal` | D-CNV-01 entity GREEN·import shadowing 해소 | — |
| **007** | [007-green-minimal-d-cnv-02-prompt](../Prompting/007-green-minimal-d-cnv-02-prompt.md) | `/green-minimal` | D-CNV-02 테스트-only GREEN·OCP 재확인 | RED 스켈레톤(`pytest.fail`) 단계 생략 — 바로 assert 작성 |

**이번 세션 핵심 인사이트**

- 두 번째 GREEN 묶음에서 **구현 코드 추가 없이** 테스트만으로 PASS → registry+Converter 설계가 FR-02 방향으로 확장 가능함을 실증
- `2.5 × METER_TO_FEET = 8.2021` → `pytest.approx(8.20210, abs=1e-5)` 로 5자리 기대값 검증
- CLI·boundary 없이 Logic Track만으로 FR-02 일부(단위 간 변환) 검증 가능

---

## 3. TDD·테스트 (Dual-Track)

**pytest 결과** (2026-06-05):

```text
python -m pytest tests/ -v
→ collected 4 items
→ 2 passed, 2 failed
```

| Phase | Test ID | Track · Layer | 파일 | 상태 |
|-------|---------|---------------|------|------|
| RED | U-IN-01 | UI · boundary | `tests/boundary/test_u_in_01.py` | 🔄 스켈레톤·FAIL |
| RED | U-IN-02 | UI · boundary | `tests/boundary/test_u_in_02.py` | 🔄 스켈레톤·FAIL |
| **GREEN** | **D-CNV-01** | Logic · entity | `tests/entity/test_d_cnv_01.py` | ✅ PASS |
| **GREEN** | **D-CNV-02** | Logic · entity | `tests/entity/test_d_cnv_02.py` | ✅ **PASS** (이번 세션) |
| RED | D-CNV-03, D-REG-01, D-CFG-01 | Logic | — | ❌ 미착수 |
| RED | U-IN-03, U-OUT-01 | UI | — | ❌ 미착수 |
| REFACTOR | — | — | — | 해당 없음 |

**D-CNV-02 검증 요약**

| 항목 | 값 |
|------|-----|
| Given | `meter`(1.0 m), `feet`(1/`METER_TO_FEET`), 입력 2.5 |
| When | `converter.convert("meter", "feet", 2.5)` |
| Then | `8.20210` (±1e-5) |

**TC 작성 팁**

- D-CNV-01과 동일 Registry 구성 패턴 재사용 — Given 블록 일관성 유지
- Logic GREEN은 `constants.METER_TO_FEET` import로 SSOT 준수 (하드코딩 금지)
- entity 2건 PASS 후 `tests/entity/` 회귀 실행으로 Track 단위 검증

---

## 4. 클린코드·리팩토링

| 항목 | 상태 |
|------|------|
| OCP (NFR-01) | ✅ D-CNV-02 GREEN에 `converter.py` **수정 없음** |
| SRP (NFR-02) | ✅ entity 4파일 분리 유지 |
| `/refactor-smell` | 미사용 |
| `/refactor-safe` | 미사용 |

**장점**: 두 번째 Test ID 추가 시 변환기 본문 비수정 — OCP 설계 가설 검증  
**어려움**: `pytest.mark.d_cnv_02` 미등록 경고 — REFACTOR 후보 (`pyproject.toml` marks)

---

## 5. 다음 단계

1. **D-CNV-03** — feet→yard, meter 경유 일치 (`/red-skeleton` → `/green-minimal`)
2. **U-IN-01~02** — boundary Track GREEN (`src/boundary/` CLI·E001/E002)
3. **REFACTOR 후보** — `pyproject.toml` custom marks · Registry fixture 공통화
4. **EXT** — `units.json`(D-CFG-01), 동적 등록(D-REG-01), `--format`(U-OUT-01)
