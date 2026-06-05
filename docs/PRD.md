# UnitConverter — Product Requirements Document (PRD)

- **버전**: 0.1 (초안)
- **작성일**: 2026-06-05
- **SSOT**: `README.md` · 본 문서 · `.cursor/skills/unit-converter-tdd/reference.md`
- **문제 정의**: [`Report/01.UnitConverter_ProblemDefinition_Report.md`](../Report/01.UnitConverter_ProblemDefinition_Report.md)

---

## 1. 배경 · 진짜 문제

해외 스펙과 국내 실측·발주 단위가 섞인 상태에서 **확실한 기준 없이** 수동 계산·해석을 반복하다 **시간·오차·책임 리스크**가 반복 발생한다.

**주제 (한 문장)**

> 해외 스펙과 국내 실측·발주 단위가 섞일 때, 손 계산·해석 반복으로 잃는 시간과 틀린 숫자 비용을, **한 번 입력으로 여러 단위를 일관되게 맞추는 것**으로 줄인다.

---

## 2. R-G-I-O

| 항목 | 내용 |
|------|------|
| **Role** | 해외 제품 스펙(inch·feet)과 국내 시공·발주 단위(mm·m)를 같은 날 맞춰야 하는 견적·발주 담당자 |
| **Goal** | 한 값 입력으로 모든 등록 단위에 대해 같은 기준·비율로 환산; 수동 확인·재계산·발주 오류 리스크 감소 |
| **Input** | `단위이름:숫자` (예: `meter:2.5`); CLI 인자 또는 대화형 입력 |
| **Output** | 등록된 **전 단위** 변환 결과 목록 (P0: 텍스트 줄; P1: `--format json \| csv \| table`) |

---

## 3. 성공 기준 (P0)

| # | 기준 | 검증 |
|---|------|------|
| SC-01 | **정확성** — README 비율·meter 경유 일관 | D-CNV-01~03, U-OUT-01 |
| SC-02 | **신뢰** — 잘못된 입력은 결과 없이 명확한 오류 | U-IN-01~03, FR-03~05 |
| SC-03 | **확장·재현** — 동적 등록·설정 오류 명확화 | D-REG-01, D-CFG-01, EXT-01~02 |

---

## 4. 범위

### In Scope (P0)

- 길이 단위 CLI: `meter`, `feet`, `yard`
- 입력 형식 `unit:value` 파싱 및 검증
- 전 단위 변환 출력
- OCP·SRP 아키텍처 (`unit_converter/` 패키지)
- Dual-Track 테스트 (Track A: CLI · Track B: Domain)

### In Scope (P1 — 추가 요구)

- `units.json` 설정 외부화 (EXT-01)
- 런타임 단위 등록 — 예: `1 cubit = 0.4572 meter` (EXT-02)
- 출력 포맷 선택 — JSON / CSV / 표 (EXT-03)

### Out of Scope

- GUI·웹·모바일 클라이언트
- 길이 이외 물리량 (질량·온도 등)
- 단위 기호 해석 (예: 6′-6″ vs 6.5 feet) — **사용자 입력 전처리**

---

## 5. 기능 요구 (FR)

| ID | 우선 | 요구 | Given | Then |
|----|------|------|-------|------|
| FR-01 | P0 | 입력 파싱 | 유효 문자열 `meter:2.5` | value=2.5, unit=meter |
| FR-02 | P0 | 전 단위 출력 | meter 2.5 | feet≈8.2021, yard≈2.7340 (README 비율) |
| FR-03 | P0 | 미지 단위 | `cubit:1` (미등록) | 명확한 오류, 변환 결과 없음 |
| FR-04 | P0 | 음수 거부 | `meter:-1` | 거부 / 예외 |
| FR-05 | P0 | 잘못된 형식 | `meter`, `abc` | 형식 오류 |

---

## 6. 비기능 요구 (NFR)

| ID | 우선 | 요구 | 검증 기준 |
|----|------|------|-----------|
| NFR-01 | P0 | OCP | 신규 단위 추가 시 **기존 변환기 코드 비수정** (register만) |
| NFR-02 | P0 | SRP | Parser / Registry / Converter / Formatter **모듈 분리** |

---

## 7. 확장 요구 (EXT)

| ID | 우선 | 요구 | Given | Then |
|----|------|------|-------|------|
| EXT-01 | P1 | 설정 파일 | `units.json` | 비율 로드; 깨진 JSON → ConfigError |
| EXT-02 | P1 | 동적 등록 | `1 cubit = 0.4572 meter` | 등록 직후 cubit 포함 전 단위 변환 |
| EXT-03 | P1 | 출력 포맷 | `--format json \| csv \| table` | 포맷별 구조·내용 검증 |

---

## 8. 비즈니스 규칙 (변환 SSOT)

```
1 meter = 3.28084 feet = 1.09361 yard
feet ↔ yard: meter 경유 (직접 상수 하드코딩 금지)
```

- 비율 상수는 `units.json` 또는 domain constants SSOT에서만 정의
- 레거시 `UnitConverter.py`에 신규 로직 추가 금지

---

## 9. 아키텍처 (목표)

```
unit_converter/
  domain/          length_unit, unit_registry, converter
  infrastructure/  config_loader
  app/             input_parser, output_formatter
  cli.py           진입점: python -m unit_converter "meter:2.5"
tests/
  test_cli.py      Track A (U-*)
  test_converter.py Track B (D-*)
```

---

## 10. 테스트 추적 (C2C)

| 요구 | Test ID |
|------|---------|
| FR-01 | U-IN-* / domain 파서 |
| FR-02 | D-CNV-01~03, U-OUT-01 |
| FR-03 | U-IN-* + 미등록 |
| FR-04 | U-IN-03 |
| FR-05 | U-IN-01, U-IN-02 |
| NFR-01 | D-REG-01 |
| NFR-02 | REFACTOR (모듈 분리) |
| EXT-01 | D-CFG-01 |
| EXT-02 | D-REG-01 |
| EXT-03 | U-OUT-01 + 포맷 확장 |

Dual-Track ID 상세: `.cursor/skills/unit-converter-tdd/reference.md`

---

## 11. 수용 기준 (Definition of Done)

- [ ] P0 FR·NFR에 대응하는 테스트 **RED → GREEN** 완료
- [ ] `pytest` 전체 PASS
- [ ] PRD ID ↔ Test ID C2C 표 팀 리뷰 확인
- [ ] P1 EXT 구현 시 동일 C2C 규칙 적용

---

## 12. 참고

| 문서 | 용도 |
|------|------|
| `README.md` | 실행·실습 Activities |
| `Report/01.UnitConverter_ProblemDefinition_Report.md` | Mom Test · R-G-I-O |
| `.cursorrules` | TDD·아키텍처 Agent 규칙 |
