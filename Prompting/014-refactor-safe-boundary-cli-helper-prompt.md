# Prompting 014 — Refactor Safe Boundary CLI Helper

- **Exported**: 2026-06-05
- **Source**: Cursor Agent session — `/refactor-safe` boundary subprocess helper 추출

---

## User

/refactor-safe

Phase: refactor | Scope: Duplicated Code — boundary subprocess harness | Track: UI

011-refactor-smell-scan에서 선택한 스멜 1개만:
- 스멜: Duplicated Code — boundary subprocess 하네스
- 위치: tests/boundary/test_u_in_01.py:12-25 · tests/boundary/test_u_in_02.py:12-25
- 작업: run_boundary_cli(args) helper 추출
- Budget: 파일 ≤3 · 클래스 0 · 함수 ≤3

원칙:
- src/** 수정 금지 — tests/만
- U-IN-01/02 stderr golden·exit code·stdout "" 계약 변경 금지
- helper는 CompletedProcess 반환 — assert는 기존 테스트에 유지
- U-IN-03 추가 구현 금지 (helper만 추출)

완료 후 /session-export:
- Report/014-refactor-safe-boundary-cli-helper-report.md
- Prompting/014-refactor-safe-boundary-cli-helper-prompt.md
- README.md 갱신

## Assistant

Phase: refactor | Scope: Duplicated Code — boundary subprocess harness | Track: UI

[Tool: Shell — pytest 4 passed 확인]

[Tool: Read — test_u_in_01.py, test_u_in_02.py, entity conftest 패턴]

**신규** `tests/boundary/conftest.py`:
- `run_boundary_cli(*cli_args)` — `subprocess.run([sys.executable, "-m", "boundary", *cli_args], …)` + PYTHONPATH=`src`

**수정** `tests/boundary/test_u_in_01.py`, `test_u_in_02.py`:
- `_SRC`·`os`·`subprocess`·`sys`·`Path` import 제거
- When subprocess 블록 → `result = run_boundary_cli("")` / `run_boundary_cli("meter")` 1줄
- Then assert(golden·exit·stdout) 유지

[Tool: Shell — pytest 4 passed + boundary golden 2건 PASS]

## TDD 완료 보고

- **Phase**: REFACTOR
- **대상 smell**: Duplicated Code — boundary subprocess harness
- **Budget**: 파일 3 / 클래스 0 / 함수 1 (`run_boundary_cli`)
- **pytest**: 4 passed — golden U-IN-01/02 matched (UPDATE_GOLDEN 없음)
- **변경 파일**: `tests/boundary/conftest.py` (신규), `tests/boundary/test_u_in_01.py`, `tests/boundary/test_u_in_02.py`
- **다음**: U-IN-03/U-OUT-01 GREEN 또는 D-CNV-03 RED
