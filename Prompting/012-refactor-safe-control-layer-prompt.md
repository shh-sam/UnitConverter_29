# Prompting 012 — Refactor Safe Control Layer

- **Session ID**: `ec1cda59-2c8c-432b-8227-3aeb9c694a6b`
- **Exported**: 2026-06-05
- **Source**: agent-transcripts/ec1cda59-2c8c-432b-8227-3aeb9c694a6b/ec1cda59-2c8c-432b-8227-3aeb9c694a6b.jsonl

---

## User

/refactor-safe

Phase: refactor | Scope: control 부재 (NFR-02) — ConvertUseCase 추출 | Track: Logic+UI

011-refactor-smell-scan에서 선택한 스멜 1개만:
- 스멜: ECB 위반 — control 레이어 부재 (NFR-02)
- 위치: src/control/__init__.py (비어 있음), src/boundary/__main__.py:main
- 작업: ConvertUseCase 스켈레톤 추출 — orchestration을 control로, boundary는 CLI I/O만
- Budget: 파일 ≤3 · 클래스 ≤1 · 메서드 ≤3

현재 동작 (변경 금지):
- parse_input("") → "E001" → stderr "E001\n", exit 1, stdout ""
- parse_input("meter") → "E002" → stderr "E002\n", exit 1, stdout ""
- parse_input("meter:2.5") → None → exit 1, stderr 없음, stdout "" (GREEN 잔재 — U-OUT-01 미구현)

완료 후 /session-export:
- Report/012-refactor-safe-control-layer-report.md
- Prompting/012-refactor-safe-control-layer-prompt.md
- README.md Prompting 표(012행)·회고 링크 갱신

## Assistant

Phase: refactor | Scope: control 부재 (NFR-02) — ConvertUseCase 추출 | Track: Logic+UI

[Tool: Shell — pytest 4 passed 확인]

[Tool: Read — __main__.py, control/__init__.py, input_parser.py]

`ConvertUseCase`를 DI(`parse_input` 콜백 주입)로 추출 — control이 boundary를 import하지 않도록 ECB 의존 방향 유지.

**신규** `src/control/convert_use_case.py`:
- `ConvertOutcome` — `error` / `not_ready` / `ready` 분류
- `ConvertUseCase.__init__(parse_input)` + `execute(raw)` — parse_input 위임·결과 분류만

**수정** `src/boundary/__main__.py`:
- argv 수집 → `ConvertUseCase(parse_input).execute(raw)` → stderr/exit code 출력만

**수정** `src/control/__init__.py` — `ConvertUseCase`, `ConvertOutcome` export

[Tool: Shell — pytest 4 passed + golden 4건 PASS]

## TDD 완료 보고

- **Phase**: REFACTOR
- **대상 smell**: ECB 위반 — control 레이어 부재 (NFR-02)
- **Budget**: 파일 3 / 클래스 1 / 메서드 2 (`__init__`, `execute`)
- **pytest**: 4 passed — golden 4건 matched (UPDATE_GOLDEN 없음)
- **변경 파일**: `src/control/convert_use_case.py` (신규), `src/boundary/__main__.py`, `src/control/__init__.py`
- **다음**: P1 테스트 fixture 중복 제거 또는 U-IN-03/U-OUT-01 GREEN
