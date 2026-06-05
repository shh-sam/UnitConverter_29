# /review-ocp-srp — OCP/SRP·C2C 리뷰 (코드 수정 금지)

UnitConverter_29 **OCP/SRP·C2C 계약**만 검사한다. **소스·테스트·설정 파일을 수정하지 않는다.** 위반은 표로만 보고한다.

## 필수 선언

**응답 첫 줄**에 아래 형식을 반드시 선언한다:

```
Phase: review | Scope: OCP/SRP·C2C | Track: Logic+UI
```

---

## 컨텍스트

| SSOT | 용도 |
|------|------|
| `@README.md` | 기능·비기능 요구 |
| `@.cursorrules` | OCP/SRP · Dual-Track · TDD 규칙 |
| `.cursor/skills/unit-converter-tdd/reference.md` | FR/NFR/EXT · Test ID · C2C |

---

## 절차 (읽기 전용)

1. **범위 스캔** — `UnitConverter.py` (레거시) · `unit_converter/` · `tests/test_cli.py` · `tests/test_converter.py`
2. **OCP 점검** — if/elif 단위 분기 잔존 · 신규 단위 추가 시 converter 비수정 여부 (NFR-01)
3. **SRP 점검** — Parser / Registry / Converter / Formatter 분리 (NFR-02)
4. **C2C 점검** — FR-01~05, NFR-01~02 각각 대응 Test ID 존재·적합성
5. **SSOT 점검** — 변환 비율 상수가 `units.json` 또는 constants에만 있는지
6. **표만 출력** — 위반 항목 + 수정 방향. 코드·commit **금지**.

---

## 검사 항목

### 1. OCP (NFR-01)

| 계약 | 허용 | 위반 |
|------|------|------|
| 신규 단위 | `LengthUnit` + `registry.register()` (또는 `units.json` 1줄) | `converter.py` 등 기존 변환기 **본문 수정** |
| 분기 | registry lookup | if/elif **단위명 하드코딩** |

### 2. SRP (NFR-02)

| 컴포넌트 | 책임 | 기대 위치 |
|----------|------|-----------|
| Parser | `unit:value` 파싱 | `app/input_parser.py` |
| Registry | 단위 등록·조회 | `domain/unit_registry.py` |
| Converter | meter 기준 변환 | `domain/converter.py` |
| Formatter | CLI 출력 | `app/output_formatter.py` |

**위반:** 한 모듈에 파싱+변환+출력 혼재 · `UnitConverter.py` 레거시에 신규 로직 추가

### 3. C2C — FR/NFR ↔ Test ID

| 요구 ID | 내용 | 대응 Test ID | 커버리지 |
|---------|------|--------------|----------|
| FR-01 | `meter:2.5` 파싱 | U-IN-* / domain 파서 | PASS / GAP / N/A |
| FR-02 | 전 단위 출력 | D-CNV-01~03, U-OUT-01 | … |
| FR-03 | 미지 단위 | 미등록 케이스 | … |
| FR-04 | 음수 거부 | U-IN-03 | … |
| FR-05 | 잘못된 형식 | U-IN-01, U-IN-02 | … |
| NFR-01 | OCP | D-REG-01 등 | … |
| NFR-02 | SRP | REFACTOR / 모듈 분리 | … |

### 4. 비율 SSOT

| 계약 | 허용 | 위반 |
|------|------|------|
| 정의원 | `units.json` · constants SSOT | `3.28084` 등 **리터럴 산재** |
| 규칙 | 1m = 3.28084 ft = 1.09361 yd, feet↔yard meter 경유 | 하드코딩·불일치 |

### 5. Mock 규칙

| Track | 규칙 |
|-------|------|
| Logic (`test_converter.py`) | Domain Mock **금지** |
| UI (`test_cli.py`) | Domain Mock **허용** |

---

## 보고 형식

### 요약

| 항목 | 결과 |
|------|------|
| 검사 범위 | (브랜치/경로) |
| 위반 건수 | N |
| C2C GAP | (FR/NFR ID 나열) |

### 위반 목록 (메인)

| ID | 체크 | 파일:줄 | 위반 내용 | 수정 방향 | 심각도 |
|----|------|---------|-----------|-----------|--------|
| V-01 | OCP | `…` | converter if/elif feet 분기 | registry.register 추출 | BLOCKER |
| V-02 | SRP | `…` | cli.py에 파싱+출력 혼재 | Parser/Formatter 분리 | MAJOR |
| V-03 | C2C | — | FR-04 테스트 없음 | U-IN-03 RED 추가 | MAJOR |
| V-04 | SSOT | `…` | 3.28084 리터럴 | units.json SSOT | MINOR |

`ID`는 `V-01`부터. **체크** 열: `OCP` · `SRP` · `C2C` · `SSOT` · `Mock`

### 체크별 PASS/FAIL

| 체크 | 결과 | 비고 |
|------|------|------|
| OCP (if/elif·converter 비수정) | PASS / FAIL | |
| SRP (4컴포넌트 분리) | PASS / FAIL | |
| C2C (FR-01~05, NFR-01~02) | PASS / GAP | |
| 비율 SSOT | PASS / FAIL | |
| Logic Track Domain Mock | PASS / FAIL / N/A | |

---

## 금지

| 금지 | 이유 |
|------|------|
| **코드·테스트·설정 수정** | 리뷰 전용 Command |
| **위반 자동 수정·GREEN/REFACTOR** | 별도 Phase |
| **git commit** | 사용자 요청 시에만 |

---

## 참고

- TDD 절차: `.cursor/skills/unit-converter-tdd/SKILL.md`
- Test ID: `.cursor/skills/unit-converter-tdd/reference.md`
- smell 탐지: `/refactor-smell` · 수정: `/refactor-safe`
