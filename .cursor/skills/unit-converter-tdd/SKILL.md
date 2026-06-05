---
name: unit-converter-tdd
description: UnitConverter Dual-Track TDD·OCP/SRP 개발 시 Agent가 따를 절차
---

# UnitConverter Dual-Track TDD

Rule SSOT: `.cursorrules` · 요구 SSOT: `README.md` · ID 목록: [reference.md](reference.md)

## 언제 이 Skill을 켜는가

| Phase | 트리거 | 모드 |
|-------|--------|------|
| **RED** | 새 Test ID, 실패 테스트 작성, `pytest.fail` 스켈레톤 | Ask (설계표) → Agent (스켈레톤) |
| **GREEN** | RED 1묶음 통과 구현, `pytest.fail` → assert 교체 | Agent |
| **REFACTOR** | 전체 PASS 후 구조 개선, smell 제거 | Ask (스멜) → Agent (추출) |
| **확장** | EXT-01~03 (`units.json`, 동적 등록, `--format`) | RED부터 새 사이클 |

작업 시작 시 **한 줄 선언** (필수):

```
Phase: red | Layer: domain | Track: Logic
```

Layer: `domain` · `app` · `infrastructure` · `cli`  
Track: `UI` (A, U-*) · `Logic` (B, D-*)

---

## Track A (U-*) vs Track B (D-*)

| | Track A — UI / Boundary | Track B — Domain / Logic |
|---|-------------------------|--------------------------|
| **ID** | U-* | D-* |
| **테스트** | `tests/test_cli.py` | `tests/test_converter.py` |
| **검증** | CLI 입출력, 형식/음수/출력 계약 | `to_meter`, `convert_all`, `register`, config load |
| **Mock** | Domain/Converter **허용** | Domain **금지** — 실제 함수 호출 |
| **RED 시** | `unit_converter/` 수정 금지 | `unit_converter/` 수정 금지 |

전체 Test ID·Given/Then: [reference.md](reference.md)

---

## OCP / SRP · Mock 규칙

**OCP**
- 새 단위 = `LengthUnit` + `registry.register()` (또는 `units.json` 1줄)
- `converter.py` 등 기존 변환기 코드 **비수정** (NFR-01)

**SRP**
- Parser · Registry · Converter · Formatter 분리 (NFR-02)
- `UnitConverter.py` 레거시에 신규 로직 추가 금지 → `unit_converter/` 패키지

**Mock**
- **Logic Track (B)**: Domain Mock **금지**
- **UI Track (A)**: Domain Mock **허용**
- RED 우회: `skip` · `xfail` · assert 완화 **금지**
- 비율 하드코딩 금지 → `units.json` 또는 constants SSOT

---

## RED 절차 (5~7단계)

1. **선언** — Phase · Layer · Track · 이번 RED 묶음 Test ID
2. **C2C 확인** — [reference.md](reference.md)에서 FR/NFR/EXT → To-Do → Test ID
   - 판단 포함 항목만 To-Do · 1 To-Do : 1 Test Case · 구현 금지
3. **Dual-Track 표** — Ask 모드, 코드 없이 표만 작성

   | Test ID | Given | Then | Expected RED Failure |
   |---------|-------|------|----------------------|

4. **파일 결정** — U-* → `tests/test_cli.py` · D-* → `tests/test_converter.py`
5. **pytest.fail 스켈레톤** — Agent, AAA 주석 + Then 한 줄:

   ```python
   def test_d_cnv_01_feet_to_meter(self):
       # Given: 1 feet
       # When: to_meter("feet", 1)
       # Then: 0.3048 m (±ε)
       pytest.fail("RED: D-CNV-01 — 구현 없음, 의도적 실패")
   ```

6. **FAIL 실행**

   ```bash
   python -m pytest tests/test_converter.py::test_d_cnv_01_feet_to_meter -v
   ```

7. **완료 보고** — [완료 보고](#완료-보고)

**금지**: `unit_converter/` 수정 · GREEN/REFACTOR 진입 · skip/xfail · 통과용 더미 assert

---

## GREEN 절차 (5~7단계)

1. **선언** — Phase · Layer · Track · 대상 RED Test ID **1묶음**
2. **RED 1묶음 선택** — 의도적 FAIL 재확인 (`pytest.fail` / NameError 등)
3. **최소 구현** — `unit_converter/`에 통과 코드만
   - 하드코딩·매직넘버 금지 · 이번 묶음 외 ID 동시 해결 금지
   - OCP: registry 확장 우선, 변환기 본문 수정 최소화
4. **assert 교체** — `pytest.fail` 제거 → 실제 assert (`pytest.approx` 허용)
5. **PASS 확인**

   ```bash
   python -m pytest tests/test_converter.py::test_d_cnv_01_feet_to_meter -v
   python -m pytest tests/test_converter.py -v
   ```

6. **회귀** (선택) — Track별 테스트 파일 전체 실행
7. **완료 보고** — 1 RED = 1 커밋 (사용자 요청 시에만)

**금지**: REFACTOR · assert 완화 · 여러 RED 한 번에 해결

---

## REFACTOR 절차 (5~7단계)

1. **선언** — `Phase: refactor | Scope: … | Track: Logic+UI`
2. **전체 PASS** — 전제 조건:

   ```bash
   python -m pytest tests/ -v
   ```

   FAIL이면 중단.

3. **smell 1개 탐지** — Ask 모드, 수정 없음

   | 우선순위 | 스멜 | 위치 | Budget 내 후보 |
   |----------|------|------|----------------|

4. **Budget 확인** — 파일 ≤ 3 · 클래스 ≤ 1 · 메서드 ≤ 3
5. **Budget 내 추출** — Agent, smell **1개만** (Extract Method / 공통 함수 / 이름 정리)
   - 입출력·CLI 계약 변경 금지 · 기능 추가·버그 수정 금지
6. **재검증** — `python -m pytest tests/ -v` → 전부 PASS
7. **완료 보고**

---

## 확장 (⑦)

EXT-01~03은 각각 **새 RED 사이클**로 진행.

| EXT | 내용 | Test ID |
|-----|------|---------|
| EXT-01 | `units.json` 비율 로드 | D-CFG-01 |
| EXT-02 | 동적 등록 `cubit=0.4572m` | D-REG-01 |
| EXT-03 | `--format json\|csv\|table` | U-OUT-01 확장 |

브랜치: `new_features` → RED → GREEN → REFACTOR → Repeat

---

## 완료 보고

매 Phase 종료 시 채팅에 보고:

```markdown
## TDD 완료 보고

- **Phase**: RED | GREEN | REFACTOR
- **Track / Layer**: …
- **Test ID**: D-CNV-01
- **pytest 결과**: `1 failed` / `N passed` (명령어 포함)
- **변경 파일**:
  - tests/test_converter.py
  - (GREEN) unit_converter/domain/converter.py
- **다음**: RED 후보 Test ID
```

---

## 추가 자료

- [reference.md](reference.md) — FR/NFR/EXT · U-* · D-* ID 목록
- `.cursorrules` — 프로젝트 헌법
- `UnitConverter.py` — 레거시 시드 (참고만)
