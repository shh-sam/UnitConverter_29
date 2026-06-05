# UnitConverter 실습 회고 보고서

- **작성일**: 2026-06-05
- **프로젝트**: UnitConverter_29
- **이번 Export 세션**: `72952094-113b-4560-a320-9023dce41c5b` → [`Prompting/010-golden-master-approval-test-prompt.md`](../Prompting/010-golden-master-approval-test-prompt.md)
- **Report 짝**: `Report/010-golden-master-approval-test-report.md`
- **Prompting 누적**: 10개 (`001` … `010`)

---

## 1. 실습 목표와 달성도

| 목표 (README Activities) | 달성 | 근거 |
|--------------------------|------|------|
| 1. 문제 코드·요구사항 분석 | ✅ | [`Report/001`](../Report/001-UnitConverter_ProblemDefinition_Report.md), [`docs/PRD.md`](../docs/PRD.md) |
| 2. OCP/SRP 기본 구현 | 🔄 | `src/entity/` 4모듈 + `src/boundary/` 2모듈 · 이번 세션 src 변경 없음 |
| 3. TC 구현 | 🔄 | D-CNV-01~02 · U-IN-01~02 GREEN PASS + **Golden Master 4건** 추가 |
| 4. 추가 요구사항 (EXT) | ❌ | EXT-01~03 미착수 |
| 5. 회고 및 발표 | 🔄 | 본 보고서·[`010-golden-master-approval-test-prompt`](../Prompting/010-golden-master-approval-test-prompt.md) |

**이번 세션 산출**

- **Golden Master 인프라**: `tests/_approval.py` — `assert_matches_golden(actual, relative)`
- **Golden 기준 파일 4개**: `tests/golden/*.approved.txt`
- **테스트 강화**: U-IN-01/02 stderr 전문 비교 · D-CNV-01/02 `pytest.approx` + 5자리 문자열 병행
- **src/** 변경 없음 — tests/ 레이어만 수정

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
| 008 | [008-green-minimal-u-in-01-prompt](../Prompting/008-green-minimal-u-in-01-prompt.md) | `/green-minimal` | U-IN-01 boundary GREEN·E001 | — |
| 009 | [009-green-minimal-u-in-02-prompt](../Prompting/009-green-minimal-u-in-02-prompt.md) | `/green-minimal` | U-IN-02 boundary GREEN·E002 | — |
| **010** | [010-golden-master-approval-test-prompt](../Prompting/010-golden-master-approval-test-prompt.md) | Agent (Golden Master) | 4건 일괄 golden·UPDATE_GOLDEN 워크플로 | `tests/__init__.py` import 보조 필요 |

**이번 세션 핵심 인사이트**

- GREEN 완료 후 **출력 계약 고정** 단계로 Golden Master 도입 — 회귀 시 diff로 원인 파악 용이
- boundary는 `result.stderr` **원문** 저장 (`E001\n`, `E002\n`) — `in` 검사보다 엄격
- entity는 `pytest.approx`(수치 허용) + `f"{result:.5f}"` golden(표시 형식 고정) **이중 검증**
- golden 갱신은 `UPDATE_GOLDEN=1` 환경변수로만 — 수동 편집 우회 방지

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
| **Golden** | **U-IN-01** | UI · boundary | `tests/boundary/test_u_in_01.py` | ✅ PASS + golden |
| **Golden** | **U-IN-02** | UI · boundary | `tests/boundary/test_u_in_02.py` | ✅ PASS + golden |
| **Golden** | **D-CNV-01** | Logic · entity | `tests/entity/test_d_cnv_01.py` | ✅ PASS + golden |
| **Golden** | **D-CNV-02** | Logic · entity | `tests/entity/test_d_cnv_02.py` | ✅ PASS + golden |
| RED | D-CNV-03, D-REG-01, D-CFG-01 | Logic | — | ❌ 미착수 |
| RED | U-IN-03, U-OUT-01 | UI | — | ❌ 미착수 |
| REFACTOR | — | — | — | 해당 없음 |

**Golden 파일 요약**

| 파일 | 내용 | 검증 대상 |
|------|------|-----------|
| `u_in_01_empty.approved.txt` | `E001\n` | CLI 빈 입력 stderr |
| `u_in_02_missing_colon.approved.txt` | `E002\n` | 콜론 누락 stderr |
| `d_cnv_01_feet_to_meter.approved.txt` | `0.30480` | 1 feet → meter (5자리) |
| `d_cnv_02_meter_to_feet.approved.txt` | `8.20210` | 2.5 meter → feet (5자리) |

**TC 작성 팁**

- Golden은 **프로덕션 변경 없이** tests/만으로 출력 계약을 고정하는 안전망
- D-CNV는 부동소수점 `approx`와 표시 문자열 golden을 병행 — 수치·포맷 각각 검증
- golden 재생성: PowerShell `$env:UPDATE_GOLDEN = "1"` → 대상 pytest → `Remove-Item Env:UPDATE_GOLDEN`

---

## 4. 클린코드·리팩토링

- Golden 인프라는 `tests/_approval.py` 단일 모듈로 캡슐화 — 테스트 파일은 `assert_matches_golden()` 한 줄 호출
- `src/**` 미변경으로 OCP/SRP 구조 유지 — 테스트 강화만 수행
- `/refactor-smell`, `/refactor-safe` — 이번 세션 미사용

---

## 5. 다음 단계

| 항목 | 설명 |
|------|------|
| U-OUT-01 GREEN | 정상 변환 stdout golden 추가 예정 |
| U-IN-03 | 추가 입력 검증 TC |
| D-CNV-03, D-REG-01, D-CFG-01 | Logic Track RED |
| EXT-01~03 | 설정 외부화·동적 등록·출력 포맷 |
| pytest marks | `u_in_01` 등 custom mark `pyproject.toml` 등록으로 warning 제거 |
