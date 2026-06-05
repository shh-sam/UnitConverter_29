# Prompting 013 — Refactor Safe Entity Registry Fixture

- **Exported**: 2026-06-05
- **Source**: Cursor Agent session — `/refactor-safe` entity Registry fixture 추출

---

## User

/refactor-safe

Phase: refactor | Scope: Duplicated Code — entity Registry 셋업 | Track: Logic

011-refactor-smell-scan에서 선택한 스멜 1개만:
- 스멜: Duplicated Code — entity Registry 셋업
- 위치: tests/entity/test_d_cnv_01.py:17-20 · tests/entity/test_d_cnv_02.py:17-20
- 작업: tests/entity/conftest.py에 meter+feet Registry fixture 추출
- Budget: 파일 ≤3 · 클래스 0 · 메서드/fixture ≤3

원칙:
- src/** 수정 금지 — tests/만
- D-CNV-01/02 변환값·pytest.approx·golden 계약 변경 금지
- fixture 이름: meter_feet_registry

완료 후 /session-export:
- Report/013-refactor-safe-entity-registry-fixture-report.md
- Prompting/013-refactor-safe-entity-registry-fixture-prompt.md
- README.md 갱신

## Assistant

Phase: refactor | Scope: Duplicated Code — entity Registry 셋업 | Track: Logic

[Tool: Shell — pytest 4 passed 확인]

[Tool: Read — test_d_cnv_01.py, test_d_cnv_02.py]

**신규** `tests/entity/conftest.py`:
- `@pytest.fixture def meter_feet_registry()` — UnitRegistry에 meter·feet 등록 후 `Converter` 반환

**수정** `tests/entity/test_d_cnv_01.py`, `test_d_cnv_02.py`:
- Given 4줄(Registry 셋업) → `converter = meter_feet_registry` 1줄
- entity import 제거 — fixture가 셋업 담당

[Tool: Shell — pytest 4 passed + entity golden 2건 PASS]

## TDD 완료 보고

- **Phase**: REFACTOR
- **대상 smell**: Duplicated Code — entity Registry 셋업
- **Budget**: 파일 3 / 클래스 0 / fixture 1 (`meter_feet_registry`)
- **pytest**: 4 passed — golden D-CNV-01/02 matched (UPDATE_GOLDEN 없음)
- **변경 파일**: `tests/entity/conftest.py` (신규), `tests/entity/test_d_cnv_01.py`, `tests/entity/test_d_cnv_02.py`
- **다음**: P1 boundary subprocess fixture 중복 또는 U-IN-03/U-OUT-01 GREEN
