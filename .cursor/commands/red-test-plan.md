# /red-test-plan — Dual-Track RED 설계표

UnitConverter_29 **Dual-Track TDD** — RED 설계표만 출력한다. **코드·테스트 파일을 만들지 않는다.**

## 필수 선언

**응답 첫 줄**에 아래 형식을 반드시 선언한다:

```
Phase: red | Layer: {{layer}} | Track: {{track}}
```

| 필드 | 값 |
|------|-----|
| **Phase** | `red` (고정) |
| **Layer** | `entity` · `control` · `boundary` 중 하나 |
| **Track** | `Logic` (B, D-*) · `UI` (A, U-*) |
| **이번 RED 묶음** | `{{test_ids}}` (예: D-CNV-01, FR-01) |

---

## 역할 · 컨텍스트 · 과제

| 구분 | 내용 |
|------|------|
| **[P] 역할** | Dual-Track TDD 전문가. Phase: **RED** (설계만). |
| **[C] 컨텍스트** | `@README.md` · `@.cursorrules` · `@UnitConverter.py` · `.cursor/skills/unit-converter-tdd/reference.md` |
| **[T] 과제** | 이번 RED 묶음: `{{test_ids}}` — **설계표만** 출력. `tests/` · `src/` 파일 생성·수정 **금지**. |
| **[F] 출력** | 아래 [보고 형식](#보고-형식) Markdown 표 4종 |

---

## 절차 (Ask 모드 — 읽기 전용)

1. **선언** — Phase · Layer · Track · Test ID 묶음 확정.
2. **C2C 확인** — `reference.md`에서 FR/NFR/EXT → To-Do → Test ID 매핑. 판단 항목만 To-Do, **1 To-Do : 1 Test Case**.
3. **Dual-Track 표** — Track B(Logic) 또는 Track A(UI) 중 해당 Track RED 설계표 작성. **Expected RED Failure** 포함.
4. **테스트 플랜** — 파일명 · 함수명 · pytest 명령.
5. **OCP/SRP 점검** — 이번 RED가 아키텍처 규칙에 부합하는지 표로 기록.
6. **표만 출력** — 구현·스켈레톤·pytest 실행 없음.

---

## 보고 형식

아래 **4개 표**를 순서대로 채운다.

### 1. C2C (Concept-to-Code)

| PRD ID | 요구 인용 (README/reference) | To-Do (1개) | Test ID | Given | When | Then |
|--------|------------------------------|-------------|---------|-------|------|------|
| FR-01 | … | … | … | … | … | … |

### 2. Track RED 설계표

Track B → `tests/entity/` · `tests/control/` · Track A → `tests/boundary/`

| Test ID | Given | When | Then | Expected RED Failure |
|---------|-------|------|------|----------------------|
| D-CNV-01 | … | … | … | `pytest.fail` / ImportError / NameError 등 |

### 3. 테스트 플랜

| Test ID | 파일 | 함수명 | pytest 명령 |
|---------|------|--------|-------------|
| D-CNV-01 | `tests/entity/` | `test_d_cnv_01_…` | `python -m pytest tests/entity/test_d_cnv_01.py::test_d_cnv_01_… -v` |

### 4. OCP/SRP 점검

| 항목 | 이번 RED 영향 | 준수 여부 | 비고 |
|------|---------------|-----------|------|
| OCP (NFR-01) | registry 확장 vs converter 수정 | PASS / 주의 | |
| SRP (NFR-02) | Parser/Registry/Converter/Formatter | PASS / 주의 | |
| Mock 규칙 | Logic Track Domain Mock 금지 | PASS / 위반 | |
| 비율 SSOT | 하드코딩 없음 | PASS / 주의 | |

---

## 금지

| 금지 | 이유 |
|------|------|
| **`tests/` · `src/` 파일 생성·수정** | 설계표 Command — 스켈레톤은 `/red-skeleton` |
| **src 구현 · GREEN · REFACTOR** | RED 설계 단계만 |
| **skip · xfail · assert 완화** | RED 우회 금지 |
| **여러 Track 혼합 설계 (명시 없을 때)** | Track A/B 중 요청 Track만 |

---

## 참고

- TDD 절차: `.cursor/skills/unit-converter-tdd/SKILL.md`
- Test ID·C2C: `.cursor/skills/unit-converter-tdd/reference.md`
- SSOT: `.cursorrules`, `README.md`
