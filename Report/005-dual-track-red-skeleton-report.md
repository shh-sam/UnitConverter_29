# UnitConverter 실습 회고 보고서

- **작성일**: 2026-06-05
- **프로젝트**: UnitConverter_29
- **이번 Export 세션**: `273780ac-41e7-47fe-8558-3c92204ab1ff` → [`Prompting/005-dual-track-red-skeleton-prompt.md`](../Prompting/005-dual-track-red-skeleton-prompt.md)
- **Report 짝**: `Report/005-dual-track-red-skeleton-report.md`
- **Prompting 누적**: 5개 (`001`, `002`, `003`, `004`, `005`)

---

## 1. 실습 목표와 달성도

| 목표 (README Activities) | 달성 | 근거 |
|--------------------------|------|------|
| 1. 문제 코드·요구사항 분석 | ✅ | [`Report/001`](../Report/001-UnitConverter_ProblemDefinition_Report.md), [`docs/PRD.md`](../docs/PRD.md) |
| 2. OCP/SRP 기본 구현 | 🔄 | `src/{entity,control,boundary}/` Harness만 (`__init__.py` 0바이트), **도메인·CLI 구현 없음** |
| 3. TC 구현 | 🔄 | **RED 스켈레톤 3건** 작성·`pytest.fail` FAIL 확인 — GREEN 미착수 |
| 4. 추가 요구사항 (EXT) | ❌ | EXT-01~03 미착수 |
| 5. 회고 및 발표 | 🔄 | 본 보고서·[`005-dual-track-red-skeleton-prompt`](../Prompting/005-dual-track-red-skeleton-prompt.md) |

**이번 세션 산출**

- `/red-skeleton` — 세션 003 설계표 기준 **D-CNV-01**, **U-IN-01**, **U-IN-02** AAA 스켈레톤 (`tests/`만 수정)
- `src/**` · `UnitConverter.py` **미수정** (RED Phase 준수)

---

## 2. AI 활용 — 도움이 된 순간과 한계

| 순번 | Prompting | 활용 Command/Skill | 도움이 된 점 | 한계 |
|------|-----------|-------------------|-------------|------|
| 001 | [001-mom-test-문제정의-prd](../Prompting/001-mom-test-문제정의-prd.md) | Ask | Mom Test·PRD SSOT | — |
| 002 | [002-ecb-harness-rules-alignment](../Prompting/002-ecb-harness-rules-alignment.md) | Agent | ECB Harness·`.cursorrules` | Hook 미구현 |
| 003 | [003-dual-track-red-test-plan-prompt](../Prompting/003-dual-track-red-test-plan-prompt.md) | `/red-test-plan` | RED 설계표·C2C·Expected Failure | — |
| 004 | [004-magic-square-ssot-cleanup-prompt](../Prompting/004-magic-square-ssot-cleanup-prompt.md) | Ask·`/session-export` | 003 Magic Square 혼입 정리 | — |
| **005** | [005-dual-track-red-skeleton-prompt](../Prompting/005-dual-track-red-skeleton-prompt.md) | `/red-skeleton` | 003 설계→스켈레톤 일괄 착수·3 failed 확인 | Test ID 묶음 미지정 시 3건 동시 작성 |

**이번 세션 핵심 인사이트**

- Ask(003) → Agent(005) Phase 분리로 **설계표 없이 스켈레톤만** 넣는 실수 방지
- `Prompting/003`·`Report/003`를 SSOT로 삼아 FR-02→D-CNV-01, FR-05→U-IN-01~02 매핑 유지

---

## 3. TDD·테스트 (Dual-Track)

**pytest 결과** (2026-06-05):

```text
python -m pytest tests/ -v
→ collected 3 items, 3 failed (의도적 pytest.fail)
```

| Phase | Test ID | Track · Layer | 파일 | 상태 |
|-------|---------|---------------|------|------|
| RED | D-CNV-01 | Logic · entity | `tests/entity/test_d_cnv_01.py` | ✅ 스켈레톤·FAIL |
| RED | U-IN-01 | UI · boundary | `tests/boundary/test_u_in_01.py` | ✅ 스켈레톤·FAIL |
| RED | U-IN-02 | UI · boundary | `tests/boundary/test_u_in_02.py` | ✅ 스켈레톤·FAIL |
| RED | D-CNV-02~03, D-REG-01, D-CFG-01 | Logic | — | ❌ 미착수 |
| RED | U-IN-03, U-OUT-01 | UI | — | ❌ 미착수 |
| GREEN / REFACTOR | — | — | — | 해당 없음 |

**스켈레톤 요약**

| Test ID | Given (주석) | When (주석) | Then |
|---------|--------------|-------------|------|
| D-CNV-01 | 1 feet, Registry | `Converter.convert("feet", "meter", 1)` | `pytest.fail("RED: D-CNV-01 — …")` |
| U-IN-01 | CLI `""` | `python -m boundary ""` | `pytest.fail("RED: U-IN-01 — …")` |
| U-IN-02 | CLI `"meter"` | `python -m boundary "meter"` | `pytest.fail("RED: U-IN-02 — …")` |

**TC 작성 팁**

- RED Then은 **`pytest.fail` 한 줄만** — GREEN에서 assert·subprocess로 교체
- Logic Track: GREEN 시 Domain Mock 금지, `src/entity/` 실제 호출
- UI Track: GREEN 시 `subprocess`로 stderr `E001`/`E002`·exit code 검증
- `@pytest.mark.*` 미등록 시 `PytestUnknownMarkWarning` — `pyproject.toml` marks 등록은 REFACTOR 후보

---

## 4. 클린코드·리팩토링

| 항목 | 상태 |
|------|------|
| ECB Harness | `src/entity|control|boundary/__init__.py`만 존재 |
| OCP/SRP | 구현 전 — RED 스켈레톤만 |
| `/refactor-smell`, `/refactor-safe` | 미사용 (PASS 0건) |

---

## 5. 다음 단계

1. **`/green-minimal`** — D-CNV-01 1묶음 (`src/entity/` 최소 구현 + assert 교체)
2. **UI Track GREEN** — U-IN-01 또는 U-IN-02 (`src/boundary/` + subprocess)
3. **RED 후보** — D-CNV-02~03, D-REG-01, D-CFG-01, U-IN-03, U-OUT-01
4. **Hook** — RED Phase `src/**` 편집 차단 (`.cursor/hooks.json`)
5. **pytest marks** — `pyproject.toml`에 `d_cnv_01`, `u_in_01` 등 등록 (선택)
