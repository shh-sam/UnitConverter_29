# UnitConverter 실습 회고 보고서

- **작성일**: 2026-06-05
- **프로젝트**: UnitConverter_29
- **이번 Export 세션**: [`Prompting/014-refactor-safe-boundary-cli-helper-prompt.md`](../Prompting/014-refactor-safe-boundary-cli-helper-prompt.md)
- **Report 짝**: `Report/014-refactor-safe-boundary-cli-helper-report.md`
- **Prompting 누적**: 14개 (`001` … `014`)

---

## 1. 실습 목표와 달성도

| 목표 (README Activities) | 달성 | 근거 |
|--------------------------|------|------|
| 1. 문제 코드·요구사항 분석 | ✅ | [`Report/001`](../Report/001-UnitConverter_ProblemDefinition_Report.md), [`011`](../Report/011-refactor-smell-scan-report.md) P1 boundary smell 식별 |
| 2. OCP/SRP 기본 구현 | 🔄 | entity OCP 충족 · control `ConvertUseCase` 스켈레톤([`012`](../Report/012-refactor-safe-control-layer-report.md)) |
| 3. TC 구현 | 🔄 | 4건 PASS + Golden Master · U-IN-03, U-OUT-01 미착수 |
| 4. 추가 요구사항 (EXT) | ❌ | EXT-01~03 미착수 |
| 5. 회고 및 발표 | 🔄 | 본 보고서·[`014-refactor-safe-boundary-cli-helper-prompt`](../Prompting/014-refactor-safe-boundary-cli-helper-prompt.md) |

**이번 세션 산출**

- **REFACTOR** (`/refactor-safe`) — P1 smell 1건: boundary subprocess 하네스 중복 제거
- `tests/boundary/conftest.py` — `run_boundary_cli(*cli_args)` helper 추출
- U-IN-01/02 subprocess 블록 → helper 1줄로 교체
- `src/**` **미수정** · stderr golden·exit code·stdout "" 계약 유지

---

## 2. AI 활용 — 도움이 된 점과 한계

| 순번 | Prompting | 활용 Command/Skill | 도움이 된 점 | 한계 |
|------|-----------|-------------------|-------------|------|
| 001~013 | [001](../Prompting/001-mom-test-문제정의-prd.md) … [013](../Prompting/013-refactor-safe-entity-registry-fixture-prompt.md) | RED/GREEN/REFACTOR | Dual-Track·Golden·entity fixture DRY | — |
| **014** | [014-refactor-safe-boundary-cli-helper-prompt](../Prompting/014-refactor-safe-boundary-cli-helper-prompt.md) | `/refactor-safe` | 011 P1 boundary 후보를 tests-only Budget 내 1 helper로 해소 | U-IN-03 RED는 별도 GREEN 사이클 필요 |

**이번 세션 핵심 인사이트**

- UI Track subprocess 테스트에서 PYTHONPATH·`capture_output` 설정은 **When 공통 전제** — `run_boundary_cli`가 SSOT
- helper가 `CompletedProcess`를 반환하면 테스트 본문은 Then(assert)에만 집중 — entity fixture 패턴과 대칭
- REFACTOR는 `tests/`만 수정해도 동일 Budget·계약 원칙 적용 — src 변경 없이 smell 제거 가능

---

## 3. TDD·테스트 (Dual-Track)

**pytest 결과** (2026-06-05):

```text
python -m pytest tests/ -v
→ collected 4 items → 4 passed

python -m pytest tests/boundary/test_u_in_01.py tests/boundary/test_u_in_02.py -v
→ 2 passed — Golden matched (UPDATE_GOLDEN 없음)
```

| Phase | Test ID | Track · Layer | 상태 |
|-------|---------|---------------|------|
| GREEN + Golden | U-IN-01, U-IN-02 | UI · boundary | ✅ PASS |
| GREEN + Golden | D-CNV-01, D-CNV-02 | Logic · entity | ✅ PASS |
| **REFACTOR** | — | boundary subprocess DRY | ✅ 완료 |
| **REFACTOR** | — | entity fixture DRY ([`013`](../Report/013-refactor-safe-entity-registry-fixture-report.md)) | ✅ 완료 |
| RED | U-IN-03, U-OUT-01 | UI · boundary | ❌ 미착수 |
| RED | D-CNV-03, D-REG-01, D-CFG-01 | Logic | ❌ 미착수 |

**TC 작성 팁**

- `run_boundary_cli("meter")` — 추가 인자는 `*cli_args`로 전달; U-OUT-01 `--format` RED 시 동일 helper 재사용
- boundary conftest는 entity conftest와 분리 — 레이어별 harness SSOT

---

## 4. 클린코드·리팩토링

### OCP/SRP 적용 경험

| 영역 | 상태 | 비고 |
|------|------|------|
| entity (NFR-01) | ✅ | REFACTOR 범위 외 — 미수정 |
| tests/entity | ✅ | [`013`](../Report/013-refactor-safe-entity-registry-fixture-report.md) fixture DRY |
| control (NFR-02) | 🔄 | [`012`](../Report/012-refactor-safe-control-layer-report.md) 스켈레톤 유지 |
| tests/boundary | ✅ | subprocess harness DRY — `conftest.py` `run_boundary_cli` |

### `/refactor-safe` 사용

- **대상**: P1 boundary subprocess 하네스 중복 (011 스캔 3순위)
- **Budget**: 파일 3 · 클래스 0 · 함수 1 (`run_boundary_cli`)
- **변경 파일**: `tests/boundary/conftest.py` (신규), `tests/boundary/test_u_in_01.py`, `tests/boundary/test_u_in_02.py`

---

## 5. 다음 단계

| 우선순위 | 작업 | Command |
|----------|------|---------|
| 1 | U-IN-03 (E003), U-OUT-01 (FR-02 출력) — UseCase에 변환·출력 연동 | `/green-minimal` |
| 2 | D-CNV-03, D-REG-01, D-CFG-01 | RED/GREEN |
| 3 | EXT-01~03 | RED부터 |
| 4 | 011 P2 smell (Formatter·Parser 등) | `/refactor-smell` → `/refactor-safe` |
