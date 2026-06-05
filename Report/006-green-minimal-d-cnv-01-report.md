# UnitConverter 실습 회고 보고서

- **작성일**: 2026-06-05
- **프로젝트**: UnitConverter_29
- **이번 Export 세션**: `b2cf06da-549b-4673-87cb-d95fb0282e49` → [`Prompting/006-green-minimal-d-cnv-01-prompt.md`](../Prompting/006-green-minimal-d-cnv-01-prompt.md)
- **Report 짝**: `Report/006-green-minimal-d-cnv-01-report.md`
- **Prompting 누적**: 6개 (`001`, `002`, `003`, `004`, `005`, `006`)

---

## 1. 실습 목표와 달성도

| 목표 (README Activities) | 달성 | 근거 |
|--------------------------|------|------|
| 1. 문제 코드·요구사항 분석 | ✅ | [`Report/001`](../Report/001-UnitConverter_ProblemDefinition_Report.md), [`docs/PRD.md`](../docs/PRD.md) |
| 2. OCP/SRP 기본 구현 | 🔄 | **첫 GREEN** — `src/entity/` 4모듈 (`LengthUnit`, `UnitRegistry`, `Converter`, `constants`) · control/boundary 미구현 |
| 3. TC 구현 | 🔄 | D-CNV-01 **GREEN PASS** · U-IN-01~02 **RED** 유지 |
| 4. 추가 요구사항 (EXT) | ❌ | EXT-01~03 미착수 |
| 5. 회고 및 발표 | 🔄 | 본 보고서·[`006-green-minimal-d-cnv-01-prompt`](../Prompting/006-green-minimal-d-cnv-01-prompt.md) |

**이번 세션 산출**

- `/green-minimal` — **D-CNV-01** 1묶음 GREEN (FR-02 / SC-01: 1 feet → 0.3048 m)
- `src/entity/` 최소 ECB entity 레이어 구현 (registry 기반 meter 경유 변환)
- `tests/conftest.py` + `tests/entity/__init__.py` 삭제 — import shadowing 해소

---

## 2. AI 활용 — 도움이 된 순간과 한계

| 순번 | Prompting | 활용 Command/Skill | 도움이 된 점 | 한계 |
|------|-----------|-------------------|-------------|------|
| 001 | [001-mom-test-문제정의-prd](../Prompting/001-mom-test-문제정의-prd.md) | Ask | Mom Test·PRD SSOT | — |
| 002 | [002-ecb-harness-rules-alignment](../Prompting/002-ecb-harness-rules-alignment.md) | Agent | ECB Harness·`.cursorrules` | Hook 미구현 |
| 003 | [003-dual-track-red-test-plan-prompt](../Prompting/003-dual-track-red-test-plan-prompt.md) | `/red-test-plan` | RED 설계표·C2C | — |
| 004 | [004-magic-square-ssot-cleanup-prompt](../Prompting/004-magic-square-ssot-cleanup-prompt.md) | `/session-export` | SSOT 혼입 정리 | — |
| 005 | [005-dual-track-red-skeleton-prompt](../Prompting/005-dual-track-red-skeleton-prompt.md) | `/red-skeleton` | RED 스켈레톤 3건 | — |
| **006** | [006-green-minimal-d-cnv-01-prompt](../Prompting/006-green-minimal-d-cnv-01-prompt.md) | `/green-minimal` | RED→GREEN 1묶음·OCP registry 설계·shadowing 진단 | import 충돌은 Harness 설계 시 사전 예고 없었음 |

**이번 세션 핵심 인사이트**

- GREEN 1묶음 원칙 준수: D-CNV-01만 해결, U-IN-01~02·D-CNV-02+ 미착수
- `tests/entity/__init__.py` + `tests/` on `sys.path` → `entity`가 `src/entity` 대신 테스트 패키지로 resolve
- `tests/conftest.py`의 `pytest_configure` + `tests/entity/__init__.py` 제거로 안정적 import

---

## 3. TDD·테스트 (Dual-Track)

**pytest 결과** (2026-06-05):

```text
python -m pytest tests/ -v
→ collected 3 items
→ 1 passed, 2 failed
```

| Phase | Test ID | Track · Layer | 파일 | 상태 |
|-------|---------|---------------|------|------|
| RED | U-IN-01 | UI · boundary | `tests/boundary/test_u_in_01.py` | 🔄 스켈레톤·FAIL |
| RED | U-IN-02 | UI · boundary | `tests/boundary/test_u_in_02.py` | 🔄 스켈레톤·FAIL |
| **GREEN** | **D-CNV-01** | Logic · entity | `tests/entity/test_d_cnv_01.py` | ✅ **PASS** |
| RED | D-CNV-02~03, D-REG-01, D-CFG-01 | Logic | — | ❌ 미착수 |
| RED | U-IN-03, U-OUT-01 | UI | — | ❌ 미착수 |
| REFACTOR | — | — | — | 해당 없음 |

**구현 요약 (D-CNV-01)**

| 컴포넌트 | 모듈 | 역할 |
|----------|------|------|
| SSOT | `src/entity/constants.py` | `METER_TO_FEET`, `METER_TO_YARD` |
| 도메인 | `src/entity/length_unit.py` | `LengthUnit(name, meters_per_unit)` |
| Registry | `src/entity/registry.py` | `UnitRegistry.register()` / `get()` |
| Converter | `src/entity/converter.py` | meter 경유 `convert(from, to, value)` |

**TC 작성 팁**

- Logic GREEN: 테스트에서 Registry 직접 구성 + `Converter` 실제 호출 (Mock 금지)
- `tests/<layer>/` 디렉터리명이 `src/<layer>/` 패키지명과 같으면 `__init__.py` 제거 또는 `conftest` path 우선 필요
- 비율은 `constants.py` SSOT 참조 — 테스트·구현 모두 `METER_TO_FEET` import

---

## 4. 클린코드·리팩토링

| 항목 | 상태 |
|------|------|
| OCP (NFR-01) | ✅ Converter 본문 고정 — 신규 단위는 `registry.register()` 확장 |
| SRP (NFR-02) | ✅ entity 4파일 분리 (constants · LengthUnit · Registry · Converter) |
| `/refactor-smell` | 미사용 |
| `/refactor-safe` | 미사용 |

**장점**: registry + meter 경유 변환으로 D-REG-01(동적 등록) 확장 경로 확보  
**어려움**: Harness `tests/entity/`와 `src/entity/` 네이밍 충돌 — REFACTOR 후보 (`pyproject.toml` marks 등록, default registry fixture)

---

## 5. 다음 단계

1. **D-CNV-02** — RED 스켈레톤 (`2.5 m → feet`, 8.20210) → `/green-minimal`
2. **U-IN-01~02** — boundary Track GREEN (`src/boundary/` CLI·E001/E002)
3. **REFACTOR 후보** — `pyproject.toml` custom marks 등록 · default `UnitRegistry` conftest fixture
4. **EXT** — `units.json`(D-CFG-01), 동적 등록(D-REG-01), `--format`(U-OUT-01)
