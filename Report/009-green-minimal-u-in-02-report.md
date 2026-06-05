# UnitConverter 실습 회고 보고서

- **작성일**: 2026-06-05
- **프로젝트**: UnitConverter_29
- **이번 Export 세션**: `ea038c4b-203d-4a8c-b4f9-43377f414543` → [`Prompting/009-green-minimal-u-in-02-prompt.md`](../Prompting/009-green-minimal-u-in-02-prompt.md)
- **Report 짝**: `Report/009-green-minimal-u-in-02-report.md`
- **Prompting 누적**: 9개 (`001` … `009`)

---

## 1. 실습 목표와 달성도

| 목표 (README Activities) | 달성 | 근거 |
|--------------------------|------|------|
| 1. 문제 코드·요구사항 분석 | ✅ | [`Report/001`](../Report/001-UnitConverter_ProblemDefinition_Report.md), [`docs/PRD.md`](../docs/PRD.md) |
| 2. OCP/SRP 기본 구현 | 🔄 | `src/entity/` 4모듈 + `src/boundary/` 2모듈 · entity Converter 본문 비수정 유지 |
| 3. TC 구현 | 🔄 | D-CNV-01~02 · **U-IN-01~02 GREEN PASS** · boundary 입력 검증 2건 완료 |
| 4. 추가 요구사항 (EXT) | ❌ | EXT-01~03 미착수 |
| 5. 회고 및 발표 | 🔄 | 본 보고서·[`009-green-minimal-u-in-02-prompt`](../Prompting/009-green-minimal-u-in-02-prompt.md) |

**이번 세션 산출**

- `/green-minimal` — **U-IN-02** GREEN: 콜론 없는 CLI 입력 `"meter"` → stderr `E002`, exit≠0
- `src/boundary/input_parser.py` — `":" not in raw` → `"E002"` (E001 다음 분기 1줄)
- `tests/boundary/test_u_in_02.py` — `pytest.fail` → `subprocess` assert (U-IN-01과 동일 패턴)
- entity D-CNV-01~02 · U-IN-01 변경 없음 — 회귀 4 passed

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
| 008 | [008-green-minimal-u-in-01-prompt](../Prompting/008-green-minimal-u-in-01-prompt.md) | `/green-minimal` | U-IN-01 boundary GREEN·E001 | E002 의도적 미구현 |
| **009** | [009-green-minimal-u-in-02-prompt](../Prompting/009-green-minimal-u-in-02-prompt.md) | `/green-minimal` | U-IN-02 E002·subprocess 패턴 재사용 | PowerShell `&&` 미지원 — `;`로 분기 |

**이번 세션 핵심 인사이트**

- 008에서 의도적으로 남겨둔 U-IN-02 RED를 **1 RED = 1 GREEN** 규칙에 맞게 해소
- U-IN-01 subprocess 패턴(`PYTHONPATH=src`)을 U-IN-02에 **그대로 복제** — boundary Track TC 일관성 확보
- `parse_input` 분기 순서: `""` → E001 → `:` 없음 → E002 → (미래) 파싱·검증

---

## 3. TDD·테스트 (Dual-Track)

**pytest 결과** (2026-06-05):

```text
python -m pytest tests/ -v
→ collected 4 items
→ 4 passed
```

| Phase | Test ID | Track · Layer | 파일 | 상태 |
|-------|---------|---------------|------|------|
| **GREEN** | **U-IN-02** | UI · boundary | `tests/boundary/test_u_in_02.py` | ✅ **PASS** (이번 세션) |
| **GREEN** | U-IN-01 | UI · boundary | `tests/boundary/test_u_in_01.py` | ✅ PASS |
| **GREEN** | D-CNV-01 | Logic · entity | `tests/entity/test_d_cnv_01.py` | ✅ PASS |
| **GREEN** | D-CNV-02 | Logic · entity | `tests/entity/test_d_cnv_02.py` | ✅ PASS |
| RED | D-CNV-03, D-REG-01, D-CFG-01 | Logic | — | ❌ 미착수 |
| RED | U-IN-03, U-OUT-01 | UI | — | ❌ 미착수 |
| REFACTOR | — | — | — | 해당 없음 |

**U-IN-02 검증 요약**

| 항목 | 값 |
|------|-----|
| Given | CLI 인자 `"meter"` (콜론 없음) |
| When | `python -m boundary "meter"` (subprocess, PYTHONPATH=src) |
| Then | stderr `E002`, exit≠0, stdout 변환 결과 없음 |

**TC 작성 팁**

- boundary GREEN은 RED 스켈레톤(`pytest.fail`) → subprocess assert 교체가 표준 흐름
- E002는 E001과 동일하게 `__main__.py`가 stderr 출력·exit 1 처리 — parser만 확장
- `abc`(E005) 등 다른 형식 오류는 **이번 묶음에서 동시 처리하지 않음** (1 RED 규칙)

---

## 4. 클린코드·리팩토링

| 항목 | 상태 |
|------|------|
| OCP (NFR-01) | ✅ entity `Converter` 본문 미수정 · boundary 입력 검증만 확장 |
| SRP (NFR-02) | 🔄 `input_parser.py`에 형식 검증 누적 · control·Formatter 미구현 |
| ECB 의존 방향 | ✅ boundary만 수정 — entity/control import 없음 |
| `/refactor-smell` | 미사용 |
| `/refactor-safe` | 미사용 |

**장점**: E001·E002 오류 계약이 boundary parser에 순차적으로 쌓임 — entity 오류 emit 없음 (`.cursorrules` 준수)  
**어려움**: U-IN-01·02의 `_SRC`·subprocess 보일러플레이트 중복 — REFACTOR 후보(conftest fixture)

---

## 5. 다음 단계

1. **U-IN-03** — `meter:-1` → stderr E003 (`/red-skeleton` → `/green-minimal`)
2. **D-CNV-03** — feet→yard meter 경유 일치 (`/red-skeleton` → `/green-minimal`)
3. **REFACTOR 후보** — `pyproject.toml` custom marks · boundary subprocess `PYTHONPATH` fixture 공통화
4. **EXT** — `units.json`(D-CFG-01), 동적 등록(D-REG-01), `--format`(U-OUT-01)
