# Prompting 003 — Dual-Track RED 설계표

- **Session ID**: `bd502df9-e85c-4aff-bd58-cb813f589239`
- **Exported**: 2026-06-05 12:00
- **Source**: agent-transcripts/bd502df9-e85c-4aff-bd58-cb813f589239/bd502df9-e85c-4aff-bd58-cb813f589239.jsonl

---

## User

/red-test-plan
Phase: red | Layer: entity | Track: Logic
이번 RED 묶음: D-LOC-01 (FR-LOC-01)
다음을 표로 작성해줘. tests/·src/ 파일은 만들지 마.
1. C2C 추적 (Rule 1~3 적용)
   - PRD FR-LOC-01 인용 (docs/PRD.md)
   - To-Do 1개 (판단 포함 항목만)
   - Test ID → Given / When / Then
2. Track B (D-*) RED 설계표
   | Test ID | 대상 함수 | Given→Then | Invariant | Expected RED Failure |
3. 테스트 플랜
   - 파일: tests/entity/test_d_loc_01.py
   - test 함수명 후보
   - conftest 픽스처 (G1 격자 등, 로직 없음)
   - pytest 명령:
     python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v
   - RED 묶음 범위 (이번 1~3 ID)
4. ECB·Mock 점검
   - Logic Track → Domain Mock 금지
   - entity E001~E005 emit 금지
금지: src/ 수정, GREEN/REFACTOR, skip/xfail
완료 후: /red-skeleton 으로 넘길 준비됐다고 한 줄로 알려줘.

[첨부] cursor_commands: red-test-plan, red-skeleton

---

## Assistant

RED 설계표 작성을 위해 PRD·reference·기존 entity 테스트 패턴을 확인합니다.

[Tool: Read]
[Tool: Grep]
[Tool: Glob]

[내용 생략 — 저장소 스캔: docs/PRD.md, reference.md, MagicSquare D-LOC-01 참조]

Phase: red | Layer: entity | Track: Logic | 이번 RED 묶음: D-LOC-01 (FR-LOC-01)

**핵심 산출**

- `docs/PRD.md`에 FR-LOC-01·D-LOC-* **미등록** — 워크북(Magic Square B-3) 매핑으로 설계
- C2C: G1 격자 → `find_blank_coords` → 1-index `[(2,2),(3,3)]` row-major
- RED 묶음 D-LOC-01~03 범위 명시, 이번 설계는 D-LOC-01만
- ECB·Mock: Logic Track Domain Mock 금지, entity E001~E005 emit 금지 — PASS
- `/red-skeleton`으로 넘길 준비 완료 안내

---

## User

Phase: red | Layer: boundary | Track: UI
이번 RED 묶음: U-IN-01, U-IN-02
Track A 표: | Test ID | Given | Then | Expected RED Failure |
(U-IN-01 grid=None → E003, ModuleNotFoundError 등)

---

## Assistant

UnitConverter SSOT에서 U-IN-01·U-IN-02 정의를 확인합니다.

[Tool: Read]
[Tool: Glob]

Phase: red | Layer: boundary | Track: UI | 이번 RED 묶음: U-IN-01, U-IN-02

**SSOT 정정**: `grid=None → E003`은 Magic Square 패턴. UnitConverter reference.md 기준:

| Test ID | Given | Then | Expected RED Failure |
|---------|-------|------|----------------------|
| U-IN-01 | CLI `""` | stderr E001, exit≠0, stdout 없음 | pytest.fail / ModuleNotFoundError / ImportError |
| U-IN-02 | CLI `"meter"` (콜론 없음) | stderr E002, exit≠0, stdout 없음 | 동일 |

E003(`meter:-1`)는 U-IN-03 — 이번 묶음 범위 밖.

---

## User

/session-export

[첨부] cursor_commands: session-export

---

## Assistant

세션 Export 진행: transcript·기존 Report 번호·저장소 상태를 확인합니다.

[Tool: Glob]
[Tool: Shell — pytest]

[내용 생략 — Report·Prompting·README 생성]
