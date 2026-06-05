# UnitConverter 실습 회고 보고서

- **작성일**: 2026-06-05
- **프로젝트**: UnitConverter_29
- **이번 Export 세션**: `8e84726f-542a-401c-abfc-95025364edf5` → [`Prompting/011-refactor-smell-scan-prompt.md`](../Prompting/011-refactor-smell-scan-prompt.md)
- **Report 짝**: `Report/011-refactor-smell-scan-report.md`
- **Prompting 누적**: 11개 (`001` … `011`)

---

## 1. 실습 목표와 달성도

| 목표 (README Activities) | 달성 | 근거 |
|--------------------------|------|------|
| 1. 문제 코드·요구사항 분석 | ✅ | [`Report/001`](../Report/001-UnitConverter_ProblemDefinition_Report.md), 레거시 `UnitConverter.py` vs `src/` 대비 |
| 2. OCP/SRP 기본 구현 | 🔄 | entity는 Registry+Converter(OCP 충족) · **control 레이어 비어 있음(NFR-02 미충족)** |
| 3. TC 구현 | 🔄 | 4건 PASS + Golden Master · U-IN-03, U-OUT-01 등 미착수 |
| 4. 추가 요구사항 (EXT) | ❌ | EXT-01~03 미착수 |
| 5. 회고 및 발표 | 🔄 | 본 보고서·[`011-refactor-smell-scan-prompt`](../Prompting/011-refactor-smell-scan-prompt.md) |

**이번 세션 산출**

- **REFACTOR smell 스캔** (`/refactor-smell`) — 코드 수정 없이 P0/P1/P2 표 작성
- **pytest 전제**: 4 passed — 스캔 진행 가능 확인
- **P0 식별**: `src/control/` 비어 있음 → `ConvertUseCase` 추출 권장
- **src/ 변경 없음** — 분석·문서화만 수행

---

## 2. AI 활용 — 도움이 된 순간과 한계

| 순번 | Prompting | 활용 Command/Skill | 도움이 된 점 | 한계 |
|------|-----------|-------------------|-------------|------|
| 001~009 | [001](../Prompting/001-mom-test-문제정의-prd.md) … [009](../Prompting/009-green-minimal-u-in-02-prompt.md) | RED/GREEN | Dual-Track 기반 구축 | — |
| 010 | [010-golden-master-approval-test-prompt](../Prompting/010-golden-master-approval-test-prompt.md) | Golden Master | 출력 계약 고정 | — |
| **011** | [011-refactor-smell-scan-prompt](../Prompting/011-refactor-smell-scan-prompt.md) | `/refactor-smell` | ECB·OCP 관점 P0/P1/P2 우선순위·Budget 내 후보 도출 | Ask 모드에서 `/session-export` 불가 → Agent 모드 재실행 필요 |

**이번 세션 핵심 인사이트**

- entity 레이어는 이미 if/elif 없이 `UnitRegistry.register` 패턴 — **NFR-01(entity) 충족**
- 레거시 `UnitConverter.py:16-24`의 if/elif는 `src/`에 이식되지 않음 — ECB 전환 방향 검증됨
- **GREEN 잔재**(input_parser E001/E002만, main 성공 경로 미구현)와 **REFACTOR 대상**(control 부재)을 구분하는 것이 중요
- 테스트 중복(entity Registry 셋업, boundary subprocess)은 P1 — `/refactor-safe` 또는 테스트 REFACTOR로 분리 가능

---

## 3. TDD·테스트 (Dual-Track)

**pytest 결과** (2026-06-05):

```text
python -m pytest tests/ -v
→ collected 4 items
→ 4 passed, 4 warnings (unknown marks)
```

| Phase | Test ID | Track · Layer | 상태 |
|-------|---------|---------------|------|
| GREEN + Golden | U-IN-01, U-IN-02 | UI · boundary | ✅ PASS |
| GREEN + Golden | D-CNV-01, D-CNV-02 | Logic · entity | ✅ PASS |
| RED | U-IN-03, U-OUT-01 | UI · boundary | ❌ 미착수 |
| RED | D-CNV-03, D-REG-01, D-CFG-01 | Logic | ❌ 미착수 |
| **REFACTOR** | — | smell 스캔 완료 | 🔄 `/refactor-safe` 대기 |

**TC 작성 팁 (smell 스캔에서)**

- entity 테스트 Registry 셋업 4줄이 D-CNV-01/02에 중복 — fixture로 추출 시 GREEN 회귀 방지에 유리
- boundary subprocess 패턴도 U-IN-03 추가 전 helper 추출 권장
- smell 스캔은 **pytest PASS 전제** — REFACTOR 전 GREEN 유지가 필수

---

## 4. 클린코드·리팩토링

### OCP/SRP 적용 경험

| 영역 | 상태 | 비고 |
|------|------|------|
| entity (NFR-01) | ✅ | `Converter` 본문 비수정, `registry.register`로 단위 추가 |
| control (NFR-02) | ❌ P0 | `src/control/` 비어 있음 — `ConvertUseCase` 미존재 |
| boundary | 🔄 | Parser 부분 구현 · Formatter 없음 |
| 레거시 | 참고 | `UnitConverter.py` if/elif — src/와 대비용 |

### `/refactor-smell` 사용

- **실행**: 이번 세션에서 최초 실행
- **산출**: P0 1건 · P1 6건 · P2 4건 · 양호 3유형
- **`/refactor-safe`**: 아직 미실행 — P0 `ConvertUseCase` 추출 권장

---

## 5. 다음 단계

| 우선순위 | 작업 | Command |
|----------|------|---------|
| 1 | P0: `ConvertUseCase` 추출 (control 스켈레톤) | `/refactor-safe` |
| 2 | U-IN-03 (E003), U-OUT-01 (FR-02 출력) | `/green-minimal` |
| 3 | P1: entity/boundary 테스트 fixture 중복 제거 | `/refactor-safe` |
| 4 | D-CNV-03, D-REG-01, EXT-01~03 | RED/GREEN 순 |

**권장 `/refactor-safe` 선언 예시**

```
Phase: refactor | Scope: control 부재 (NFR-02) — ConvertUseCase 추출 | Track: Logic+UI
```
