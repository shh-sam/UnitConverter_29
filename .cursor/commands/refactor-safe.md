# /refactor-safe — 스멜 1개만 Safe Refactor

UnitConverter_29 **REFACTOR** — `/refactor-smell`에서 식별한 smell **1개만** Change Budget 내에서 안전하게 개선한다.

## 필수 선언

**응답 첫 줄**에 아래 형식을 반드시 선언한다:

```
Phase: refactor | Scope: {{smell_description}} | Track: Logic+UI
```

| 필드 | 값 |
|------|-----|
| **Phase** | `refactor` (고정) |
| **대상** | `{{smell_description}}` — smell **1개** (예: converter if/elif 단위 분기) |

---

## 전제 조건

```bash
python -m pytest tests/ -v
```

**전부 PASS**가 아니면 REFACTOR **중단**.

---

## 절차

`.cursor/skills/unit-converter-tdd/SKILL.md` **REFACTOR 절차**를 따른다.

1. **선언** — Phase · 대상 smell 1개 · Budget 확인.
2. **Budget 확인** — 파일 ≤ 3 · 클래스 ≤ 1 · 메서드 ≤ 3.
3. **Safe Refactor** — smell 1개만 처리.
   - **입출력 계약 변경 금지** — CLI 메시지 · 변환값 · 오류 형식 유지
   - **OCP/SRP** — Parser / Registry / Converter / Formatter 추출·분리
   - Extract Method · 공통 함수 · 이름 정리 (기능 동작 동일)
4. **재검증** — `python -m pytest tests/ -v` → **전부 PASS**.
5. **완료 보고** — 변경 파일·Budget 사용량·pytest 결과.

---

## 허용 리팩터 유형

| 유형 | 예시 |
|------|------|
| Extract Method | 파싱 로직 → `input_parser.py` |
| Extract Class | Formatter 분리 |
| Registry 확장 | if/elif → `registry.register()` |
| SSOT 정리 | 매직넘버 → `units.json` / constants |
| 이름 정리 | 메서드·변수명 (동작 불변) |

---

## 완료 보고

```markdown
## TDD 완료 보고

- **Phase**: REFACTOR
- **대상 smell**: converter if/elif 단위 분기
- **Budget**: 파일 2 / 클래스 0 / 메서드 2
- **pytest 결과**: `N passed` — `python -m pytest tests/ -v`
- **변경 파일**: unit_converter/domain/converter.py, unit_converter/domain/unit_registry.py
- **다음**: 남은 smell 또는 새 RED
```

---

## 금지

| 금지 | 이유 |
|------|------|
| **smell 2개 이상 동시 처리** | 1 REFACTOR = 1 smell |
| **기능 추가** | 별도 GREEN (`/green-minimal`) |
| **입출력·CLI 계약 변경** | Safe Refactor |
| **Budget 초과** | 파일 > 3 · 클래스 > 1 · 메서드 > 3 |
| **테스트 skip/xfail로 PASS 유지** | REFACTOR 우회 |
| **자동 git commit** | 사용자 요청 시에만 |

---

## 참고

- TDD 절차: `.cursor/skills/unit-converter-tdd/SKILL.md`
- smell 탐지: `/refactor-smell`
- SSOT: `.cursorrules`, `README.md`
