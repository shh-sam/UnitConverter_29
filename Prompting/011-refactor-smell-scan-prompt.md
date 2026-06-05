# Prompting 011 — Refactor Smell Scan

- **Session ID**: `8e84726f-542a-401c-abfc-95025364edf5`
- **Exported**: 2026-06-05
- **Source**: agent-transcripts/8e84726f-542a-401c-abfc-95025364edf5/8e84726f-542a-401c-abfc-95025364edf5.jsonl

---

## User

/refactor-smell

Phase: refactor | Scope: smell-scan | Track: Logic+UI

전제 확인:
python -m pytest tests/ -v
→ 전부 PASS 아니면 중단하고 알려줘.

다음 스멜 표로 src/·tests/·UnitConverter.py(레거시 참고) 스캔 (코드 수정·commit 금지):

스캔 범위:
- src/entity/ — LengthUnit, UnitRegistry, Converter, constants
- src/control/ — (현재 비어 있음 여부 확인)
- src/boundary/ — __main__, input_parser
- tests/entity/, tests/boundary/, tests/_approval.py, tests/golden/
- UnitConverter.py — 레거시 if/elif (src/와 대비만, 수정 금지)

| 우선순위 | 스멜 | 위치(파일:함수/줄) | 근거 | Change Budget 내 리팩터 후보 |
| P0/P1/P2 | ECB 위반 (boundary→entity 직접, control 부재) | | NFR-02 | ConvertUseCase 추출 |
| | Long Method (>25줄·책임2+) | | | Extract Method |
| | Duplicated Code | | | 공통 함수/fixture |
| | if/elif 단위 분기 (src/ 내) | | NFR-01/OCP | registry.register |
| | Feature Envy (boundary 도메인 로직) | | | control로 이동 |
| | Magic Number (constants 밖) | | | constants.py SSOT |
| | Incomplete Stub (GREEN 잔재) | | | Extract만, 동작 불변 |

Change Budget: 파일≤3 · 클래스≤1 · 메서드≤3

출력:
1. pytest 전제 표
2. P0/P1/P2 스멜 표
3. /refactor-safe에 넘길 후보 1~3개 (Budget 내, P0 우선)
4. "다음: P0 1개만 골라 /refactor-safe 실행" 안내

완료 후 /session-export 실행:
- Report/011-refactor-smell-scan-report.md
- Prompting/011-refactor-smell-scan-prompt.md
- README.md Prompting 표·회고 링크 갱신
(git commit·push는 내가 요청할 때만)

## Assistant

스멜 스캔을 시작합니다. 먼저 pytest 전제를 확인하고 `src/`·`tests/`·레거시 코드를 읽기 전용으로 스캔합니다.

[Tool: Shell — pytest tests/ -v]
[Tool: Glob — src/, tests/]
[Tool: Read — UnitConverter.py, entity/, boundary/, control/]
[Tool: Read — tests/entity, tests/boundary, _approval.py, conftest.py]
[Tool: Grep — if/elif, magic numbers, ECB components]

Phase: refactor | Scope: smell-scan | Track: Logic+UI

## 1. pytest 전제

| 명령 | 결과 |
|------|------|
| `python -m pytest tests/ -v` | **4 passed** (0 failed) — 스캔 진행 |

경고 4건: `@pytest.mark.d_cnv_01` 등 커스텀 마크가 `pyproject.toml`에 미등록 (`PytestUnknownMarkWarning`).

## 2. 스멜 목록 (P0 / P1 / P2)

| 우선순위 | 스멜 | 위치 (파일:함수/줄) | 근거 | Change Budget 내 리팩터 후보 |
|----------|------|---------------------|------|------------------------------|
| **P0** | ECB 위반 — control 부재 (NFR-02) | `src/control/__init__.py` (비어 있음) · `src/boundary/__main__.py:main` | NFR-02: UseCase(control) 분리 미충족. U-OUT-01 GREEN 시 boundary→entity 직접 결합 위험 | `ConvertUseCase` 추출 (파일 2) |
| **P1** | Duplicated Code — entity Registry 셋업 | `tests/entity/test_d_cnv_01.py:17-20` · `test_d_cnv_02.py:17-20` | 동일 Registry+register 반복 | `meter_feet_registry` fixture |
| **P1** | Duplicated Code — boundary subprocess 하네스 | `tests/boundary/test_u_in_01.py:12-25` · `test_u_in_02.py:12-25` | subprocess·PYTHONPATH 패턴 동일 | `run_boundary_cli()` helper |
| **P1** | Incomplete Stub (GREEN 잔재) | `src/boundary/input_parser.py:parse_input:4-9` | E001/E002만 처리, `meter:2.5`는 `None` | GREEN 대상 — REFACTOR 아님 |
| **P1** | Incomplete Stub — main 성공 경로 미구현 | `src/boundary/__main__.py:main:14-15` | 변환·출력 없음 (U-OUT-01 미구현) | UseCase 도입 시 orchestration 이동 |
| **P1** | ECB 미완 — OutputFormatter 부재 | `src/boundary/` | FR-02 3줄 출력 경로 없음 | GREEN 후 REFACTOR |
| **P1** | 레거시·ECB 이중 구현 (참고) | `UnitConverter.py:main:16-32` | if/elif·하드코딩. src/는 Registry+Converter로 OCP 충족 | 레거시 분석용 유지 |
| **P2** | Magic Number — 테스트 오라클 | `tests/entity/test_d_cnv_01.py:26` | `0.3048` constants 밖 | 우선순위 낮음 |
| **P2** | Magic Number — 미사용 상수 | `src/entity/constants.py:4` (`METER_TO_YARD`) | yard 미등록 | GREEN 시 등록 |
| **P2** | pytest 마크 미등록 | `pyproject.toml` | 4 warnings | markers 등록 |
| **P2** | UnitRegistry 미지 단위 처리 | `src/entity/registry.py:get:11-12` | `KeyError` — E004 미정 | GREEN/REFACTOR 혼합 |

**스캔에서 해당 없음 (양호)**

| 스멜 유형 | src/ 상태 |
|-----------|-----------|
| if/elif 단위 분기 | `src/` 내 없음 — 레거시만 해당 |
| Long Method (>25줄·책임 2+) | `src/` 해당 없음 |
| boundary→entity 직접 호출 | 현재 없음 — control 부재가 선행 P0 |

## 3. `/refactor-safe` 후보 (Budget 내)

| 순위 | 대상 smell | 제안 작업 | Budget |
|------|------------|-----------|--------|
| **1 (P0)** | control 부재 (NFR-02) | `ConvertUseCase` 스켈레톤 — ECB 자리만 확보 | 파일 2 · 클래스 1 · 메서드 2 |
| **2 (P1)** | entity Registry 중복 | `tests/entity/conftest.py` fixture | 파일 1 |
| **3 (P1)** | boundary subprocess 중복 | `run_boundary_cli()` helper | 파일 1 |

## 4. 다음 단계

**P0 1개만 골라 `/refactor-safe` 실행** — 권장: 「control 부재 → ConvertUseCase 추출」.

`/session-export`는 Ask 모드 제한으로 Agent 모드에서 재실행 필요 안내.

## User

/session-export

## Assistant

Phase: export | Scope: session-report | Track: Documentation

세션 Export 진행 — Transcript·Report·README 갱신.
