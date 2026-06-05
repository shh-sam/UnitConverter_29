# UnitConverter 실습 회고 보고서

- **작성일**: 2026-06-05
- **프로젝트**: UnitConverter_29
- **이번 Export 세션**: `ec1cda59-2c8c-432b-8227-3aeb9c694a6b` → [`Prompting/012-refactor-safe-control-layer-prompt.md`](../Prompting/012-refactor-safe-control-layer-prompt.md)
- **Report 짝**: `Report/012-refactor-safe-control-layer-report.md`
- **Prompting 누적**: 12개 (`001` … `012`)

---

## 1. 실습 목표와 달성도

| 목표 (README Activities) | 달성 | 근거 |
|--------------------------|------|------|
| 1. 문제 코드·요구사항 분석 | ✅ | [`Report/001`](../Report/001-UnitConverter_ProblemDefinition_Report.md), [`011`](../Report/011-refactor-smell-scan-report.md) smell 스캔 |
| 2. OCP/SRP 기본 구현 | 🔄 | entity OCP 충족 · **control `ConvertUseCase` 스켈레톤 추가(NFR-02 부분 충족)** |
| 3. TC 구현 | 🔄 | 4건 PASS + Golden Master · U-IN-03, U-OUT-01 미착수 |
| 4. 추가 요구사항 (EXT) | ❌ | EXT-01~03 미착수 |
| 5. 회고 및 발표 | 🔄 | 본 보고서·[`012-refactor-safe-control-layer-prompt`](../Prompting/012-refactor-safe-control-layer-prompt.md) |

**이번 세션 산출**

- **REFACTOR** (`/refactor-safe`) — P0 smell 1건: control 레이어 부재 해소
- `ConvertUseCase` + `ConvertOutcome` 추출 — orchestration을 control로 이동
- `boundary/__main__.py` — argv·stderr·exit code만 담당
- entity/converter/registry/constants **미수정** · CLI 계약·Golden 4건 유지

---

## 2. AI 활용 — 도움이 된 순간과 한계

| 순번 | Prompting | 활용 Command/Skill | 도움이 된 점 | 한계 |
|------|-----------|-------------------|-------------|------|
| 001~010 | [001](../Prompting/001-mom-test-문제정의-prd.md) … [010](../Prompting/010-golden-master-approval-test-prompt.md) | RED/GREEN | Dual-Track·Golden 기반 | — |
| 011 | [011-refactor-smell-scan-prompt](../Prompting/011-refactor-smell-scan-prompt.md) | `/refactor-smell` | P0 후보·Budget 예측 | — |
| **012** | [012-refactor-safe-control-layer-prompt](../Prompting/012-refactor-safe-control-layer-prompt.md) | `/refactor-safe` | ECB DI 패턴(parse_input 콜백)으로 control↔boundary 역의존 회피 | Converter 연동은 다음 GREEN 대기 |

**이번 세션 핵심 인사이트**

- control이 `parse_input`을 직접 import하면 ECB 역방향 위반 → **생성자 DI**로 boundary가 parser를 주입
- `ConvertOutcome`(`error`/`not_ready`/`ready`)로 결과 분류와 CLI I/O를 분리
- REFACTOR는 기능 추가 없이 **레이어 자리 확보**만 — U-OUT-01 GREEN 시 UseCase에 Converter 호출 추가 예정

---

## 3. TDD·테스트 (Dual-Track)

**pytest 결과** (2026-06-05):

```text
python -m pytest tests/ -v
→ collected 4 items → 4 passed

python -m pytest tests/boundary/test_u_in_01.py tests/boundary/test_u_in_02.py \
  tests/entity/test_d_cnv_01.py tests/entity/test_d_cnv_02.py -v
→ 4 passed — Golden matched (UPDATE_GOLDEN 없음)
```

| Phase | Test ID | Track · Layer | 상태 |
|-------|---------|---------------|------|
| GREEN + Golden | U-IN-01, U-IN-02 | UI · boundary | ✅ PASS |
| GREEN + Golden | D-CNV-01, D-CNV-02 | Logic · entity | ✅ PASS |
| **REFACTOR** | — | control `ConvertUseCase` 추출 | ✅ 완료 |
| RED | U-IN-03, U-OUT-01 | UI · boundary | ❌ 미착수 |
| RED | D-CNV-03, D-REG-01, D-CFG-01 | Logic | ❌ 미착수 |

**TC 작성 팁**

- boundary subprocess Golden은 REFACTOR 후에도 회귀 방지에 유효 — internal 구조 변경과 무관하게 CLI 계약 고정
- control 레이어 테스트(`tests/control/`)는 D-CFG-01 RED 시 추가 권장

---

## 4. 클린코드·리팩토링

### OCP/SRP 적용 경험

| 영역 | 상태 | 비고 |
|------|------|------|
| entity (NFR-01) | ✅ | REFACTOR 범위 외 — 미수정 |
| control (NFR-02) | 🔄 | `ConvertUseCase` 스켈레톤 — Converter 미연동 |
| boundary | 🔄 | `__main__` I/O만 · parser는 boundary 유지 |
| ECB 의존 | ✅ | `boundary → control` · control은 boundary import 없음(DI) |

### `/refactor-safe` 사용

- **대상**: P0 control 부재 (011 스캔 1순위)
- **Budget**: 파일 3 · 클래스 1 (`ConvertUseCase`) · 메서드 2 (`__init__`, `execute`)
- **변경 파일**: `src/control/convert_use_case.py`, `src/control/__init__.py`, `src/boundary/__main__.py`

---

## 5. 다음 단계

| 우선순위 | 작업 | Command |
|----------|------|---------|
| 1 | U-IN-03 (E003), U-OUT-01 (FR-02 출력) — UseCase에 변환·출력 연동 | `/green-minimal` |
| 2 | P1: entity/boundary 테스트 fixture 중복 제거 | `/refactor-safe` |
| 3 | D-CNV-03, D-REG-01, D-CFG-01 | RED/GREEN |
| 4 | EXT-01~03 | RED부터 |
