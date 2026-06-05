# Prompting 010 — Golden Master (Approval Test)

- **Session ID**: `72952094-113b-4560-a320-9023dce41c5b`
- **Exported**: 2026-06-05
- **Source**: agent-transcripts/72952094-113b-4560-a320-9023dce41c5b/72952094-113b-4560-a320-9023dce41c5b.jsonl

---

## User

UnitConverter_29 — 현재 PASS된 테스트 4건 전체에 Golden Master(Approval Test)를 구축하고 pytest로 검증해줘.

**선언**: Phase: green | Scope: Golden Master | Track: Logic + UI · Layer: boundary (U-IN-*) + entity (D-CNV-*)

**포함**: U-IN-01, U-IN-02 (stderr golden) · D-CNV-01, D-CNV-02 (convert 결과 문자열 golden, approx 병행)

**제외**: U-OUT-01 · src/** 변경 금지 · git commit 금지

**절차**: Step 0 GREEN 확인 → `tests/_approval.py` + `tests/golden/` → 테스트 연결 → `UPDATE_GOLDEN=1` 생성 → matched 검증

---

## Assistant

Golden Master 구축을 시작합니다. SSOT와 현재 테스트 상태를 먼저 확인합니다.

[Tool: Read — SKILL.md, test_u_in_01.py, test_u_in_02.py, test_d_cnv_01.py, test_d_cnv_02.py]
[Tool: Shell — pytest 4건 + tests/ (4 passed)]

Step 0 통과(4 passed). 인프라와 테스트 연결을 진행합니다.

[Tool: Glob — tests/**/*]
[Tool: Grep — _approval|assert_matches_golden (없음)]
[Tool: Read — conftest.py, pyproject.toml]

`tests/_approval.py` 생성 — `assert_matches_golden()` (UPDATE_GOLDEN=1 저장 / difflib diff 비교).
`tests/__init__.py` 생성 — `from tests._approval import ...` 패키지 import용.

4개 테스트 파일 Then 절을 golden assert로 교체·추가:
- U-IN-01/02: `result.stderr` → `.approved.txt`
- D-CNV-01/02: `f"{result:.5f}"` golden 추가 (approx 유지)

[Tool: Write — tests/_approval.py, tests/__init__.py]
[Tool: StrReplace — test_u_in_01.py, test_u_in_02.py, test_d_cnv_01.py, test_d_cnv_02.py]

Step 3: `UPDATE_GOLDEN=1`로 golden 파일 생성.

[Tool: Shell — UPDATE_GOLDEN=1 pytest 4건 (4 passed)]

[Tool: Read — golden 4개 파일]
[Tool: Shell — UPDATE_GOLDEN 제거 후 pytest 전체 (4 passed)]

**Golden Master 완료 보고**

| Golden 파일 | 내용 |
|-------------|------|
| u_in_01_empty.approved.txt | `E001\n` |
| u_in_02_missing_colon.approved.txt | `E002\n` |
| d_cnv_01_feet_to_meter.approved.txt | `0.30480` |
| d_cnv_02_meter_to_feet.approved.txt | `8.20210` |

- UPDATE_GOLDEN=1 생성: 성공
- matched 검증: 4 passed, diff 없음
- src/** 변경 없음

---

## User

/session-export

[첨부] cursor_commands: session-export
