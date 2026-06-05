# /green-minimal — 선택 RED 1묶음 최소 구현

UnitConverter_29 **Dual-Track TDD** — 선택한 RED Test ID **1묶음**만 최소 구현으로 통과시킨다.

## 필수 선언

**응답 첫 줄**에 아래 형식을 반드시 선언한다:

```
Phase: green | Test ID: {{test_id}}
```

| 필드 | 값 |
|------|-----|
| **Phase** | `green` (고정) |
| **Test ID** | `{{test_id}}` (예: D-CNV-01) — **1묶음만** |

---

## 절차

`.cursor/skills/unit-converter-tdd/SKILL.md` **GREEN 절차**를 따른다.

1. **선언** — Phase · Layer · Track · 대상 Test ID 1묶음.
2. **RED 재확인** — 대상 테스트가 **FAIL**인지 pytest로 확인 (`pytest.fail` / ImportError 등).
3. **최소 구현** — `unit_converter/`에 통과하는 코드만 추가·수정.
   - **하드코딩·매직넘버 금지** — `units.json` 또는 constants SSOT
   - **OCP**: registry 확장 우선, converter 본문 수정 최소화
   - **이번 RED 외 Test ID 동시 해결 금지**
4. **assert 교체** — `pytest.fail` 제거 → 실제 assert (`pytest.approx` 허용).
5. **PASS 확인** — 단일 테스트 → 해당 Track 테스트 파일 → (선택) 회귀.
6. **완료 보고** — pytest 결과·변경 파일. **git commit은 사용자 요청 시만.**

---

## pytest 예시

```bash
# 1. RED 재확인 (FAIL 기대)
python -m pytest tests/test_converter.py::test_d_cnv_01_feet_to_meter -v

# 2. GREEN 후 단일 PASS
python -m pytest tests/test_converter.py::test_d_cnv_01_feet_to_meter -v

# 3. Track 회귀
python -m pytest tests/test_converter.py -v
```

---

## 완료 보고

```markdown
## TDD 완료 보고

- **Phase**: GREEN
- **Track / Layer**: Logic · domain
- **Test ID**: D-CNV-01
- **pytest 결과**: `1 passed` (명령어 포함)
- **변경 파일**:
  - tests/test_converter.py (pytest.fail → assert)
  - unit_converter/domain/converter.py
- **다음**: 다음 RED 후보 Test ID
```

---

## 금지

| 금지 | 이유 |
|------|------|
| **이번 RED 외 Test ID 동시 해결** | 1 RED = 1 GREEN 묶음 |
| **REFACTOR** | 구조 개선은 `/refactor-safe` |
| **assert 완화·skip·xfail** | GREEN을 테스트 조작으로 달성 |
| **비율·단위 하드코딩** | SSOT 위반 |
| **`UnitConverter.py` 레거시에 신규 로직** | `unit_converter/` 패키지 사용 |
| **자동 git commit** | 사용자 명시 요청 시에만 |

---

## 참고

- TDD 절차: `.cursor/skills/unit-converter-tdd/SKILL.md`
- Test ID·C2C: `.cursor/skills/unit-converter-tdd/reference.md`
- SSOT: `.cursorrules`, `README.md`
