# /refactor-smell — 코드 스멜 분석 (수정 금지)

UnitConverter_29 **REFACTOR smell 탐지** — 코드를 **수정하지 않는다.** Ask 모드(읽기 전용)로 스멜만 보고한다.

## 필수 선언

**응답 첫 줄**에 아래 형식을 반드시 선언한다:

```
Phase: refactor | Scope: smell-scan | Track: Logic+UI
```

---

## 전제 조건

REFACTOR smell 분석 전, **전체 테스트 PASS** 여부를 확인한다:

```bash
python -m pytest tests/ -v
```

| 상태 | 조치 |
|------|------|
| **전부 PASS** | smell 스캔 진행 |
| **FAIL 있음** | smell 분석 **중단** — GREEN 먼저 |

---

## 절차 (읽기 전용)

1. **전제 확인** — `pytest tests/ -v` 결과 기록.
2. **스캔 범위** — `UnitConverter.py` (레거시) vs `unit_converter/` 패키지.
   - `unit_converter/domain/` — length_unit, unit_registry, converter
   - `unit_converter/app/` — input_parser, output_formatter
   - `unit_converter/infrastructure/` — config_loader
   - `unit_converter/cli.py`
3. **스멜 탐지** — OCP/SRP·중복·거대 함수·if/elif 단위 분기·하드코딩·책임 혼재.
4. **우선순위 부여** — P0 / P1 / P2.
5. **Change Budget 내 후보만** — 파일 ≤ 3 · 클래스 ≤ 1 · 메서드 ≤ 3.
6. **표만 출력** — 패치·코드 수정·commit **금지**.

---

## 보고 형식

### pytest 전제

| 명령 | 결과 |
|------|------|
| `python -m pytest tests/ -v` | N passed / FAIL — (중단 사유) |

### 스멜 목록 (메인)

| 우선순위 | 스멜 | 위치 (파일:줄) | 설명 | 리팩터 후보 (Budget 내) |
|----------|------|----------------|------|-------------------------|
| P0 | if/elif 단위 분기 | `…` | … | Registry.register 추출 |
| P1 | Parser+Formatter 혼재 | `…` | … | Formatter 분리 |
| P2 | 매직넘버 | `…` | … | constants SSOT |

**우선순위 가이드**

| 등급 | 예시 |
|------|------|
| **P0** | OCP/SRP 위반, 변환기 본문 if/elif, Logic Mock 우회 |
| **P1** | 중복 코드, 레거시·패키지 이중 구현, 책임 경계 모호 |
| **P2** | 네이밍, 소규모 Extract Method, 주석·구조 정리 |

### Change Budget 요약

| 항목 | Budget | 권장 1순위 smell |
|------|--------|------------------|
| 파일 | ≤ 3 | (P0 1건) |
| 클래스 | ≤ 1 | |
| 메서드 | ≤ 3 | |

---

## 금지

| 금지 | 이유 |
|------|------|
| **코드·테스트·설정 수정** | smell 분석 전용 |
| **기능 추가·버그 수정** | 별도 GREEN |
| **자동 REFACTOR 실행** | `/refactor-safe`에서 1건씩 |
| **git commit** | 사용자 요청 시에만 |

---

## 참고

- TDD 절차: `.cursor/skills/unit-converter-tdd/SKILL.md`
- 아키텍처: `.cursorrules`, `README.md`
- 다음 단계: `/refactor-safe` — smell 1개만 Safe Refactor
