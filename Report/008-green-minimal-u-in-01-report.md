# UnitConverter 실습 회고 보고서

- **작성일**: 2026-06-05
- **프로젝트**: UnitConverter_29
- **이번 Export 세션**: `0c60fe7c-e5c4-462d-bd8b-7f3694edb7af` → [`Prompting/008-green-minimal-u-in-01-prompt.md`](../Prompting/008-green-minimal-u-in-01-prompt.md)
- **Report 짝**: `Report/008-green-minimal-u-in-01-report.md`
- **Prompting 누적**: 8개 (`001` … `008`)

---

## 1. 실습 목표와 달성도

| 목표 (README Activities) | 달성 | 근거 |
|--------------------------|------|------|
| 1. 문제 코드·요구사항 분석 | ✅ | [`Report/001`](../Report/001-UnitConverter_ProblemDefinition_Report.md), [`docs/PRD.md`](../docs/PRD.md) |
| 2. OCP/SRP 기본 구현 | 🔄 | `src/entity/` 4모듈 + **`src/boundary/` 2모듈** (`input_parser`, `__main__`) · entity Converter 본문 비수정 유지 |
| 3. TC 구현 | 🔄 | D-CNV-01~02 · **U-IN-01 GREEN PASS** · U-IN-02 **RED** 유지 |
| 4. 추가 요구사항 (EXT) | ❌ | EXT-01~03 미착수 |
| 5. 회고 및 발표 | 🔄 | 본 보고서·[`008-green-minimal-u-in-01-prompt`](../Prompting/008-green-minimal-u-in-01-prompt.md) |

**이번 세션 산출**

- `/green-minimal` — entity D-CNV-01·02는 이미 GREEN, 추가 변경 없음 확인
- **U-IN-01** GREEN — UI Track(boundary) 첫 구현: 빈 CLI 입력 `""` → stderr `E001`, exit≠0
- `src/boundary/input_parser.py`, `src/boundary/__main__.py` 신규
- `tests/boundary/test_u_in_01.py` — `pytest.fail` → `subprocess` assert 교체

---

## 2. AI 활용 — 도움이 된 순간과 한계

| 순번 | Prompting | 활용 Command/Skill | 도움이 된 점 | 한계 |
|------|-----------|-------------------|-------------|------|
| 001 | [001-mom-test-문제정의-prd](../Prompting/001-mom-test-문제정의-prd.md) | Ask | Mom Test·PRD SSOT | — |
| 002 | [002-ecb-harness-rules-alignment](../Prompting/002-ecb-harness-rules-alignment.md) | Agent | ECB Harness·`.cursorrules` | Hook 미구현 |
| 003 | [003-dual-track-red-test-plan-prompt](../Prompting/003-dual-track-red-test-plan-prompt.md) | `/red-test-plan` | RED 설계표·E001/E002 계약 | — |
| 004 | [004-magic-square-ssot-cleanup-prompt](../Prompting/004-magic-square-ssot-cleanup-prompt.md) | `/session-export` | SSOT 혼입 정리 | — |
| 005 | [005-dual-track-red-skeleton-prompt](../Prompting/005-dual-track-red-skeleton-prompt.md) | `/red-skeleton` | RED 스켈레톤 3건 | — |
| 006 | [006-green-minimal-d-cnv-01-prompt](../Prompting/006-green-minimal-d-cnv-01-prompt.md) | `/green-minimal` | D-CNV-01 entity GREEN | — |
| 007 | [007-green-minimal-d-cnv-02-prompt](../Prompting/007-green-minimal-d-cnv-02-prompt.md) | `/green-minimal` | D-CNV-02 테스트-only GREEN | — |
| **008** | [008-green-minimal-u-in-01-prompt](../Prompting/008-green-minimal-u-in-01-prompt.md) | `/green-minimal` | U-IN-01 boundary GREEN·subprocess PYTHONPATH | E002 초안 작성 후 되돌림 — 1 RED 규칙 준수 |

**이번 세션 핵심 인사이트**

- Logic Track GREEN 완료 후 **UI Track으로 전환** — boundary 레이어 첫 실구현
- `subprocess`로 `python -m boundary` 실행 시 **PYTHONPATH=src** 필수 (pytest `pythonpath`와 subprocess 환경 분리)
- 1 RED = 1 GREEN: E002 처리를 넣었다가 **U-IN-02 동시 해결 방지** 위해 `parse_input`을 E001만 반환하도록 축소

---

## 3. TDD·테스트 (Dual-Track)

**pytest 결과** (2026-06-05):

```text
python -m pytest tests/ -v
→ collected 4 items
→ 3 passed, 1 failed
```

| Phase | Test ID | Track · Layer | 파일 | 상태 |
|-------|---------|---------------|------|------|
| **GREEN** | **U-IN-01** | UI · boundary | `tests/boundary/test_u_in_01.py` | ✅ **PASS** (이번 세션) |
| RED | U-IN-02 | UI · boundary | `tests/boundary/test_u_in_02.py` | 🔄 스켈레톤·FAIL |
| **GREEN** | D-CNV-01 | Logic · entity | `tests/entity/test_d_cnv_01.py` | ✅ PASS |
| **GREEN** | D-CNV-02 | Logic · entity | `tests/entity/test_d_cnv_02.py` | ✅ PASS |
| RED | D-CNV-03, D-REG-01, D-CFG-01 | Logic | — | ❌ 미착수 |
| RED | U-IN-03, U-OUT-01 | UI | — | ❌ 미착수 |
| REFACTOR | — | — | — | 해당 없음 |

**U-IN-01 검증 요약**

| 항목 | 값 |
|------|-----|
| Given | CLI 인자 `""` |
| When | `python -m boundary ""` (subprocess, PYTHONPATH=src) |
| Then | stderr `E001`, exit≠0, stdout 변환 결과 없음 |

**TC 작성 팁**

- UI Track GREEN은 `subprocess` + `capture_output=True`로 stderr·exit·stdout 계약 검증
- subprocess 환경에 `PYTHONPATH`를 명시하지 않으면 `No module named boundary.__main__` 발생
- boundary 테스트는 entity와 달리 **control Mock 허용** — 이번에는 parser·CLI만 최소 구현
- `parse_input`은 이번 묶음에서 `""` → `"E001"`만 처리; 나머지는 `None` (U-IN-02 선행 GREEN 방지)

---

## 4. 클린코드·리팩토링

| 항목 | 상태 |
|------|------|
| OCP (NFR-01) | ✅ entity `Converter` 본문 미수정 · boundary에 입력 검증 분리 |
| SRP (NFR-02) | 🔄 `InputParser` → `input_parser.py`, CLI → `__main__.py` (control·Formatter 미구현) |
| ECB 의존 방향 | ✅ boundary만 추가 — entity/control import 없음 (이번 GREEN 범위) |
| `/refactor-smell` | 미사용 |
| `/refactor-safe` | 미사용 |

**장점**: E001 오류 계약을 boundary에서 일관되게 처리 — entity에 오류 emit 없음 (`.cursorrules` 준수)  
**어려움**: subprocess PYTHONPATH 설정 · `pytest.mark.u_in_01` 미등록 경고 (REFACTOR 후보)

---

## 5. 다음 단계

1. **U-IN-02** — `meter`(콜론 없음) → stderr E002 (`/green-minimal`)
2. **D-CNV-03** — feet→yard meter 경유 일치 (`/red-skeleton` → `/green-minimal`)
3. **REFACTOR 후보** — `pyproject.toml` custom marks · boundary subprocess `PYTHONPATH` fixture 공통화
4. **EXT** — `units.json`(D-CFG-01), 동적 등록(D-REG-01), `--format`(U-OUT-01)
