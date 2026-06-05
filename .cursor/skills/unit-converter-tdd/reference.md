# UnitConverter — C2C 참조 (요구 · 테스트 ID)

SSOT: `README.md` · 프로젝트가이드 PDF · `.cursorrules`

## 기능 요구 (FR)

| ID | 요구 | Given | Then |
|----|------|-------|------|
| FR-01 | `meter:2.5` 파싱 | 유효 문자열 | value=2.5, unit=meter |
| FR-02 | 전 단위 출력 | meter 2.5 | feet≈8.2021, yard≈2.7340 |
| FR-03 | 미지 단위 | cubit:1 (미등록) | 명확한 오류 |
| FR-04 | 음수 거부 | meter:-1 | 거부 / 예외 |
| FR-05 | 잘못된 형식 | meter / abc | 형식 오류 |

## 비기능 요구 (NFR)

| ID | 요구 | 검증 기준 |
|----|------|-----------|
| NFR-01 | OCP | 신규 단위 추가 시 기존 변환기 코드 비수정 |
| NFR-02 | SRP | Parser / Registry / Converter / Formatter 분리 |

## 확장 요구 (EXT)

| ID | 요구 | Given | Then |
|----|------|-------|------|
| EXT-01 | 설정 파일 | units.json | 비율 로드 |
| EXT-02 | 동적 등록 | 1 cubit = 0.4572 m | 즉시 변환 가능 |
| EXT-03 | 출력 포맷 | --format json / csv / table | 포맷별 검증 |

---

## Dual-Track 테스트 ID (PDF)

파일: Track A → `tests/test_cli.py` · Track B → `tests/test_converter.py`

| Track | ID | Given | Then |
|-------|-----|-------|------|
| A | U-IN-01 | `""` | 형식 오류 |
| A | U-IN-02 | `meter` (콜론 없음) | 형식 오류 |
| A | U-IN-03 | `meter:-1` | 음수 거부 |
| A | U-OUT-01 | `meter:2.5` | 3줄 이상 출력 |
| B | D-CNV-01 | 1 feet → meter | 0.3048 m (±ε) |
| B | D-CNV-02 | 2.5 m → feet | 8.20210 (5자리) |
| B | D-CNV-03 | feet→yard | meter 경유 일치 |
| B | D-REG-01 | cubit 0.4572 등록 | 변환 가능 |
| B | D-CFG-01 | 깨진 json | ConfigError |

---

## C2C 매핑

| 요구 | Test ID |
|------|---------|
| FR-01 | (파싱) U-IN-* / domain 파서 |
| FR-02 | D-CNV-01~03, U-OUT-01 |
| FR-03 | U-IN-* + 미등록 케이스 |
| FR-04 | U-IN-03 |
| FR-05 | U-IN-01, U-IN-02 |
| NFR-01 | D-REG-01 (converter 비수정 증명) |
| NFR-02 | REFACTOR (모듈 분리) |
| EXT-01 | D-CFG-01 |
| EXT-02 | D-REG-01 |
| EXT-03 | U-OUT-01 + 포맷별 확장 |

---

## 변환 비율 SSOT

```
1 meter = 3.28084 feet = 1.09361 yard
feet ↔ yard: meter 경유
```
