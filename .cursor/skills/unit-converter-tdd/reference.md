# UnitConverter — C2C 참조 (요구 · 테스트 ID)

SSOT: `.cursorrules` · `README.md` · `docs/PRD.md`

## 기능 요구 (FR)

| ID | 요구 | Given | Then |
|----|------|-------|------|
| FR-01 | `meter:2.5` 파싱 | 유효 문자열 | value=2.5, unit=meter |
| FR-02 | 전 단위 출력 | meter 2.5 | feet≈8.2021, yard≈2.7340 |
| FR-03 | 미지 단위 | cubit:1 (미등록) | E004, 변환 없음 |
| FR-04 | 음수 거부 | meter:-1 | E003, 거부 |
| FR-05 | 잘못된 형식 | meter / abc / meter:abc | E002 / E005 / E007 |

## 비기능 요구 (NFR)

| ID | 요구 | 검증 기준 |
|----|------|-----------|
| NFR-01 | OCP | 신규 단위 추가 시 변환기 본문 비수정 |
| NFR-02 | SRP | Parser/Formatter(boundary) · Registry/Converter(entity) · UseCase(control) 분리 |

## 확장 요구 (EXT)

| ID | 요구 | Given | Then |
|----|------|-------|------|
| EXT-01 | 설정 파일 | units.json | 비율 로드 |
| EXT-02 | 동적 등록 | 1 cubit = 0.4572 m | 즉시 변환 가능 |
| EXT-03 | 출력 포맷 | --format json / csv / table | 포맷별 검증 |

---

## 오류 코드 E001~E007

| 코드 | Given | Then | Test ID |
|------|-------|------|---------|
| E001 | `""` | 형식 오류 | U-IN-01 |
| E002 | `meter` (콜론 없음) | 형식 오류 | U-IN-02 |
| E003 | `meter:-1` | 음수 거부 | U-IN-03 |
| E004 | `cubit:1` (미등록) | 미지 단위 | FR-03 |
| E005 | `abc` | 형식 오류 | FR-05 |
| E006 | 깨진 json | ConfigError | D-CFG-01 |
| E007 | `meter:abc` | 값 비숫자 | FR-05 |

오류 출력: stderr `E00x` · exit ≠ 0 · stdout 변환 결과 없음

---

## Dual-Track 테스트 ID

| Track | Layer | 디렉터리 | ID | Given | Then |
|-------|-------|----------|-----|-------|------|
| A | boundary | `tests/boundary/` | U-IN-01 | `""` | E001 |
| A | boundary | `tests/boundary/` | U-IN-02 | `meter` (콜론 없음) | E002 |
| A | boundary | `tests/boundary/` | U-IN-03 | `meter:-1` | E003 |
| A | boundary | `tests/boundary/` | U-OUT-01 | `meter:2.5` | 3줄 이상 출력 |
| B | entity | `tests/entity/` | D-CNV-01 | 1 feet → meter | 0.3048 m (±ε) |
| B | entity | `tests/entity/` | D-CNV-02 | 2.5 m → feet | 8.20210 (5자리) |
| B | entity | `tests/entity/` | D-CNV-03 | feet→yard | meter 경유 일치 |
| B | entity | `tests/entity/` | D-REG-01 | cubit 0.4572 등록 | 변환 가능 |
| B | control | `tests/control/` | D-CFG-01 | 깨진 json | E006 / ConfigError |

---

## ECB 컴포넌트 매핑

| 컴포넌트 | 레이어 | 기대 모듈 |
|----------|--------|-----------|
| LengthUnit, Registry, Converter | entity | `src/entity/` |
| ConvertUseCase, ConfigLoad | control | `src/control/` |
| CLI, InputParser, OutputFormatter | boundary | `src/boundary/` |

---

## C2C 매핑

| 요구 | Test ID |
|------|---------|
| FR-01 | U-IN-* / boundary 파서 |
| FR-02 | D-CNV-01~03, U-OUT-01 |
| FR-03 | E004 / 미등록 케이스 |
| FR-04 | U-IN-03 (E003) |
| FR-05 | U-IN-01~02, E005, E007 |
| NFR-01 | D-REG-01 (converter 본문 비수정) |
| NFR-02 | REFACTOR (ECB 모듈 분리) |
| EXT-01 | D-CFG-01 |
| EXT-02 | D-REG-01 |
| EXT-03 | U-OUT-01 + 포맷 확장 |

---

## 변환 비율 SSOT

```
1 meter = 3.28084 feet = 1.09361 yard
feet ↔ yard: meter 경유
```
