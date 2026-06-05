# /red-skeleton — RED 테스트 스켈레톤만

UnitConverter_29 **Dual-Track TDD** — RED 테스트 스켈레톤만 작성한다. **구현 코드는 수정하지 않는다.**

## 필수 선언

**응답 첫 줄**에 아래 형식을 반드시 선언한다:

```
Phase: red | Track: {{track}} | Test IDs: {{test_ids}}
```

| 필드 | 값 |
|------|-----|
| **Phase** | `red` (고정) |
| **Track** | `Logic` (B, D-*) · `UI` (A, U-*) |
| **Test IDs** | `{{test_ids}}` (예: D-CNV-01, D-CNV-02) |

---

## 절차

`.cursor/skills/unit-converter-tdd/SKILL.md` **RED 절차**를 따른다.

1. **선언** — Phase · Track · Test ID 묶음.
2. **파일 결정** — U-* → `tests/test_cli.py` · D-* → `tests/test_converter.py`
3. **AAA 스켈레톤 작성** — `tests/` 아래에만 추가·수정.
   - **Given / When / Then** 주석 (AAA)
   - **Then** 본문은 **한 줄만**:

     ```python
     pytest.fail("RED: [Test ID] — …")
     ```

   - docstring 또는 `@pytest.mark`에 Test ID 명시.
4. **`unit_converter/` 수정 금지** — 프로덕션·패키지 코드 손대지 않음.
5. **pytest FAIL 실행** — 대상 테스트 실행 후 **반드시 실패** 확인.
6. **완료 보고** — SKILL [완료 보고](#완료-보고) 형식.

---

## 스켈레톤 예시

```python
def test_d_cnv_01_feet_to_meter(self):
    # Given: 1 feet
    # When: to_meter("feet", 1)
    # Then: 0.3048 m (±ε)
    pytest.fail("RED: D-CNV-01 — 구현 없음, 의도적 실패")
```

---

## pytest 예시

```bash
# Logic Track — 단일 테스트
python -m pytest tests/test_converter.py::test_d_cnv_01_feet_to_meter -v

# Logic Track — 파일 전체
python -m pytest tests/test_converter.py -v

# UI Track
python -m pytest tests/test_cli.py::test_u_in_01_empty_input -v
```

RED 직후 통과하면 테스트가 너무 약하거나 이미 구현됨 — assert·대상 ID 재확인.

---

## 완료 보고

```markdown
## TDD 완료 보고

- **Phase**: RED
- **Track / Layer**: Logic · domain
- **Test ID**: D-CNV-01
- **pytest 결과**: `1 failed` (명령어 포함)
- **변경 파일**: tests/test_converter.py
- **다음**: `/green-minimal` — 해당 Test ID 최소 구현
```

---

## 금지

| 금지 | 이유 |
|------|------|
| **`unit_converter/` · `UnitConverter.py` 수정** | RED는 실패 테스트만 |
| **Logic Track Domain Mock** | 실제 domain 함수 호출 |
| **실제 assert (GREEN용)** | 스켈레톤은 `pytest.fail` 한 줄만 |
| **skip · xfail · assert 완화 · 테스트 삭제** | RED 우회 |
| **GREEN · REFACTOR 동시 진행** | Phase 분리 |

---

## 참고

- TDD 절차: `.cursor/skills/unit-converter-tdd/SKILL.md`
- Test ID: `.cursor/skills/unit-converter-tdd/reference.md`
