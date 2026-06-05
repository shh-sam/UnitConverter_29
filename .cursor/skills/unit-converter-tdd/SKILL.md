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
Phase: red | Layer: entity | Track: Logic
```

Layer: `entity` · `control` · `boundary`  
Track: `UI` (A, U-*) · `Logic` (B, D-*)

---

## Track A (U-*) vs Track B (D-*)

| | Track A — UI / Boundary | Track B — Logic (entity + control) |
|---|-------------------------|-------------------------------------|
| **ID** | U-* | D-* |
| **테스트** | `tests/boundary/` | `tests/entity/` · `tests/control/` |
| **검증** | CLI·E00x·출력·--format | to_meter, convert, register, config load |
| **Mock** | control **허용** | entity/control **금지** — 실제 호출 |
| **RED 시** | `src/**` 수정 금지 | `src/boundary/` 수정 금지 |

전체 Test ID·Given/Then·E00x: [reference.md](reference.md)

---

## OCP / SRP · Mock 규칙

**OCP**
- 새 단위 = `LengthUnit` + `registry.register()` (또는 `units.json` 1줄)
- Converter 등 변환기 **본문 비수정** (NFR-01)

**SRP (ECB)**
- entity: Registry · Converter · LengthUnit
- control: 유스케이스·설정 로드 흐름
- boundary: CLI · Parser · Formatter
- `UnitConverter.py` 레거시에 신규 로직 금지 → `src/` ECB

**Mock**
- **Logic Track (B)**: entity/control Mock **금지**
- **UI Track (A)**: control Mock **허용**
- RED 우회: `skip` · `xfail` · assert 완화 **금지**
- 비율 하드코딩 금지 → `units.json` 또는 constants SSOT

---

## Test/Review Loop (pytest)

| Phase | 명령 | 기대 |
|-------|------|------|
| RED | `python -m pytest tests/<layer>/test_<…>.py::<func> -v` | **FAIL** |
| GREEN | 동일 → `pytest tests/<layer>/ -v` | 대상 **PASS** |
| REFACTOR | `python -m pytest tests/ -v` | **전부 PASS** |
| REVIEW | pytest·파일 수정 **금지** | `/review-ocp-srp` |

---

## RED 절차 (5~7단계)

1. **선언** — Phase · Layer · Track · 이번 RED 묶음 Test ID
2. **C2C 확인** — [reference.md](reference.md)에서 FR/NFR/EXT → To-Do → Test ID
3. **Dual-Track 표** — Ask 모드, 코드 없이 표만 작성
4. **파일 결정** —
   - U-* → `tests/boundary/`
   - D-CNV-*, D-REG-* → `tests/entity/`
   - D-CFG-* → `tests/control/`
5. **pytest.fail 스켈레톤** — Agent, AAA 주석 + Then 한 줄
6. **FAIL 실행**
7. **완료 보고**

**금지**: `src/**` 수정 · GREEN/REFACTOR 진입 · skip/xfail · 통과용 더미 assert

---

## GREEN 절차 (5~7단계)

1. **선언** — Phase · Layer · Track · 대상 RED Test ID **1묶음**
2. **RED 1묶음 선택** — 의도적 FAIL 재확인
3. **최소 구현** — `src/<layer>/`에 통과 코드만
4. **assert 교체** — `pytest.fail` 제거 → 실제 assert
5. **PASS 확인** — 단일 → Track 디렉터리
6. **회귀** (선택) — `pytest tests/ -v`
7. **완료 보고** — 1 RED = 1 커밋 (사용자 요청 시에만)

**금지**: REFACTOR · assert 완화 · 여러 RED 한 번에 해결

---

## REFACTOR 절차 (5~7단계)

1. **선언** — `Phase: refactor | Scope: … | Track: Logic+UI`
2. **전체 PASS** — `python -m pytest tests/ -v` (FAIL이면 중단)
3. **smell 1개 탐지** — Ask 모드
4. **Budget 확인** — 파일 ≤ 3 · 클래스 ≤ 1 · 메서드 ≤ 3
5. **Budget 내 추출** — 입출력·E00x 계약 변경 금지
6. **재검증** — `pytest tests/ -v` 전부 PASS
7. **완료 보고**

---

## 확장 (⑦)

EXT-01~03은 각각 **새 RED 사이클**로 진행.

| EXT | 내용 | Test ID |
|-----|------|---------|
| EXT-01 | `units.json` 비율 로드 | D-CFG-01 |
| EXT-02 | 동적 등록 `cubit=0.4572m` | D-REG-01 |
| EXT-03 | `--format json\|csv\|table` | U-OUT-01 확장 |

---

## 완료 보고

```markdown
## TDD 완료 보고

- **Phase**: RED | GREEN | REFACTOR
- **Track / Layer**: …
- **Test ID**: D-CNV-01
- **pytest 결과**: `1 failed` / `N passed` (명령어 포함)
- **변경 파일**:
  - tests/entity/test_d_cnv_01.py
  - (GREEN) src/entity/converter.py
- **다음**: RED 후보 Test ID
```

---

## 추가 자료

- [reference.md](reference.md) — FR/NFR/EXT · U-* · D-* · E00x
- `.cursorrules` — 프로젝트 헌법
- `UnitConverter.py` — 레거시 시드 (참고만)
