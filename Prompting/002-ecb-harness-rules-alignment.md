# Prompting 002 — ECB Harness 및 Rules 정렬

- **Session ID**: `fcb065f8-a046-4234-8d2f-a8199870c9de`
- **Exported**: 2026-06-05 10:19
- **Source**: agent-transcripts/fcb065f8-a046-4234-8d2f-a8199870c9de/fcb065f8-a046-4234-8d2f-a8199870c9de.jsonl

---

## User

ECB + Dual-Track TDD용 최소 Harness를 만들어줘.
- pyproject.toml (pytest만)
- src/boundary, src/control, src/entity (빈 __init__.py)
- tests/entity, tests/control, tests/boundary (빈 __init__.py)
- Report/01, Report/02 는 이미 있다고 가정
코드·테스트 본문은 아직 작성하지 마. Harness 골격만.

---

## Assistant

Dual-Track TDD용 ECB Harness 골격을 맞추기 위해 프로젝트 스킬과 기존 구조를 먼저 확인합니다.

[내용 생략]

[Tool: Read]
[Tool: Glob]
[Tool: Read]

---

## Assistant

[내용 생략]

[Tool: Read]
[Tool: Read]
[Tool: Glob]

---

## Assistant

[내용 생략]

[Tool: Grep]
[Tool: Read]

---

## Assistant

[내용 생략]

[Tool: Read]

---

## Assistant

ECB + Dual-Track TDD용 최소 Harness 골격을 생성합니다.

[내용 생략]

[Tool: Write]
[Tool: Write]
[Tool: Write]
[Tool: Write]
[Tool: Write]
[Tool: Write]
[Tool: Write]

---

## Assistant

[내용 생략]

[Tool: Shell]

---

## Assistant

[내용 생략]

[Tool: Shell]

---

## Assistant

ECB + Dual-Track TDD용 최소 Harness 골격을 만들었습니다.

## 생성된 구조

```
UnitConverter_29/
├── pyproject.toml
├── src/
│   ├── entity/__init__.py
│   ├── control/__init__.py
│   └── boundary/__init__.py
└── tests/
    ├── entity/__init__.py
    ├── control/__init__.py
    └── boundary/__init__.py
```

## `pyproject.toml` 요약

- **의존성**: `dev` extra에 `pytest>=8.0,<9`만 포함
- **pytest 설정**: `testpaths = ["tests"]`, `pythonpath = ["src"]` (src 레이아웃)

## 검증

`python -m pytest tests/ -v` 실행 시 `pyproject.toml`이 설정으로 로드되고, 테스트 본문이 없어 `0 items collected`로 정상 종료됩니다 (exit code 5).

Report/01·02는 요청대로 건드리지 않았습니다. RED 단계에서 `tests/entity`, `tests/control`, `tests/boundary` 아래에 Test ID별 스켈레톤을 추가하면 됩니다.

[내용 생략]

---

## User

아래 .cursorrules 초안을 리뷰만 해. 파일 수정하지 마.
[초안 전문 붙여넣기]
Rule(헌법) 관점 체크:
- ECB import 방향
- Logic vs UI Track Mock
- 입출력·E001~E007
- TDD 게이트·금지 사항
- Test/Review Loop와 연결될 pytest 규칙
- Hook과 겹칠 규칙 (예: Golden Master 재생성 승인)
| 우선순위 | 추가/수정 문장 | 이유 |

---

## Assistant

초안 본문이 붙여넣어지지 않았습니다. 프로젝트의 기존 규칙·스킬·Hook을 읽고 리뷰 기준에 맞춰 점검합니다.

[내용 생략]

[Tool: Read]
[Tool: Glob]
[Tool: Grep]

---

## Assistant

[내용 생략]

[Tool: Grep]
[Tool: Read]
[Tool: Glob]
[Tool: Read]

---

## Assistant

[내용 생략]

[Tool: Read]
[Tool: Grep]
[Tool: Read]

---

## Assistant

[내용 생략]

[Tool: Read]
[Tool: Glob]
[Tool: Glob]

---

## Assistant

[내용 생략]

[Tool: Grep]

---

## Assistant

[내용 생략]

[Tool: Grep]
[Tool: Read]

---

## Assistant

[내용 생략]

[Tool: Glob]
[Tool: Grep]

---

## Assistant

[내용 생략]

[Tool: Grep]
[Tool: Read]

---

## Assistant

[내용 생략]

[Tool: Glob]
[Tool: Glob]

---

## Assistant

[내용 생략]

[Tool: Read]
[Tool: Read]

---

## Assistant

[내용 생략]

[Tool: Grep]

---

## Assistant

**초안 본문이 붙여넣어지지 않았습니다** (`[초안 전문 붙여넣기]` 자리만 있음). 아래는 요청하신 6개 Rule(헌법) 관점으로 **현재 `.cursorrules` + ECB Harness + Skill/Command**를 기준선으로 삼은 **갭 리뷰**입니다. 초안 문장 단위 판정은 초안 전문을 주시면 이어서 할 수 있습니다.

---

## 관점별 점검 (현재 상태 vs 헌법에 있어야 할 것)

### 1. ECB import 방향
**현재 `.cursorrules`**: `unit_converter/domain·app·infrastructure` — ECB·import 규칙 **없음**.  
**Harness**: `src/entity`, `src/control`, `src/boundary`만 존재.

헌법에 **한 줄로 고정**해야 할 방향:

```text
boundary → control → entity  (안쪽으로만 의존)
entity: control/boundary import 금지
control: entity만 import, boundary import 금지
boundary: control(및 entity 간접)만 import
```

**누락 시 리스크**: Agent가 `entity`에서 `argparse`/`print`를 넣거나, `control`이 `boundary`를 import하는 **순환·레이어 침범**이 TDD 중 반복됩니다.

---

### 2. Logic vs UI Track · Mock
**현재**: Track A/B + Mock 규칙은 Skill·`/review-ocp-srp`에만 있고, `.cursorrules`에는 Mock **없음**.  
**경로 불일치**: Skill/Command는 `tests/test_cli.py` / `tests/test_converter.py`인데 Harness는 `tests/{entity,control,boundary}/`.

헌법 표는 **Track ↔ Layer ↔ 테스트 디렉터리**를 한 표로 묶어야 합니다:

| Track | Layer | 테스트 | Mock |
|-------|-------|--------|------|
| B Logic | entity + control | `tests/entity/`, `tests/control/` | Entity/Control **Mock 금지** |
| A UI | boundary | `tests/boundary/` | Control **Mock 허용** (Boundary는 실제 I/O만) |

**RED 시 수정 금지 범위**도 Track별로 적어야 합니다: Logic RED → `src/boundary/` 금지, UI RED → `src/entity/` 직접 수정 금지 등.

---

### 3. 입출력 · E001~E007
**저장소에 E001~E007 정의 없음** (Report/02·PDF 미동봉). FR/U-IN과의 대응은 헌법 **필수 SSOT 표**입니다.

PRD·reference 기준 **최소 매핑 후보** (초안과 다르면 Report/02 기준으로 덮어쓰기):

| 코드 | Given (예) | Then (계약) | Test ID |
|------|------------|-------------|---------|
| E001 | `""` | 형식 오류, 변환 없음 | U-IN-01 |
| E002 | `meter` (콜론 없음) | 형식 오류 | U-IN-02 |
| E003 | `meter:-1` | 음수 거부 | U-IN-03 |
| E004 | `cubit:1` (미등록) | 미지 단위 | FR-03 |
| E005 | `abc` 등 | 형식/값 오류 | FR-05 |
| E006 | 깨진 `units.json` | ConfigError, 잘못된 숫자 금지 | D-CFG-01 |
| E007 | (초안/Report/02 SSOT) | — | — |

헌법에 **반드시** 넣을 계약 3가지:
- **입력**: `unit:value` (R-G-I-O SSOT)
- **성공 출력**: 등록 전 단위 목록 (P0 텍스트 / P1 `--format`)
- **오류 출력**: `E00x` **코드·메시지·exit code** (stdout/stderr 중 어디에 쓸지 명시)

---

### 4. TDD 게이트 · 금지 사항
**현재 `.cursorrules`**: RED/GREEN/REFACTOR·금지 4줄 — **양호**. ECB·Harness와 맞추려면 **수정 금지 경로**만 갱신 필요.

| Phase | 허용 | 금지 (헌법에 명시 권장) |
|-------|------|-------------------------|
| RED | `tests/**` only | `src/**` 전부 (또는 Track별 세분) |
| GREEN | 이번 RED 1묶음 대응 `src/**` | 다른 Test ID 동시 해결, skip/xfail |
| REFACTOR | Change Budget 내 구조 | 동작·E00x·출력 계약 변경 |

**SSOT 역할 분리**도 한 줄 필요: `.cursorrules` = 원칙, `SKILL.md` = 절차, `reference.md` = ID·Given/Then. 지금 Skill이 “Rule SSOT: `.cursorrules`”라고 하는데 Rule 내용이 Skill보다 빈약하면 Agent가 Skill만 따릅니다.

---

### 5. Test/Review Loop · pytest 규칙
Skill에 “Test/Review Loop pytest 명령”이 언급됐으나 **현재 SKILL.md 본문에는 구체 명령 블록 없음**. 헌법(또는 Rule→Skill 위임)에 **최소 게이트**를 고정하는 것이 좋습니다:

```text
RED:    pytest tests/<layer>/test_<id>.py::<func> -v  → 반드시 FAIL
GREEN:  동일 + pytest tests/<layer>/ -v              → 해당 Track PASS
REFACTOR: pytest tests/ -v                         → 전 Track PASS
REVIEW: pytest 실행·파일 수정 금지 (/review-ocp-srp)
```

`pyproject.toml`의 `pythonpath = ["src"]`와 **테스트 네이밍**(`test_<test_id>.py` vs flat)도 Rule 한 줄로 고정하면 Loop가 흔들리지 않습니다.

---

### 6. Hook과 겹칠 규칙 (Golden Master 등)
**프로젝트에 `.cursor/hooks.json` 없음** — Hook은 아직 미구현.

헌법 vs Hook **역할 분담** 권장:

| 주제 | `.cursorrules` (원칙) | Hook (강제) |
|------|----------------------|-------------|
| Golden Master 재생성 | “스냅샷 변경은 **사용자 명시 승인** 없이 금지” | `afterFileEdit` / `beforeShellExecution`에서 `tests/**/golden/**` diff 차단 |
| RED에서 src 수정 | “RED는 tests만” | `afterFileEdit`에서 `src/**` 편집 경고·거부 |
| pytest skip/xfail | “RED 우회 금지” | 편집 후 `@pytest.mark.skip` 패턴 감지 |

**중복 금지**: Hook이 막는 것과 Rule이 금지하는 것을 **같은 문장으로 두 번** 쓰지 말고, Rule은 “왜”, Hook은 “어떻게 막는지”만.

---

## 우선순위 표 (초안에 **추가·수정** 권장 문장)

| 우선순위 | 추가/수정 문장 (초안에 넣을 내용) | 이유 |
|:--------:|----------------------------------|------|
| **P0** | `## SSOT 계층`: `.cursorrules`(헌법) → `reference.md`(ID) → `SKILL.md`(절차) → `Commands`(실행). 충돌 시 `.cursorrules` 우선. | Skill/Command가 이미 더 상세해 Rule이 사실상 무시됨 |
| **P0** | `## 아키텍처 (ECB)`: `src/boundary` → `src/control` → `src/entity` 단방향 import. 역방향·횡단 import 금지. | Harness와 legacy `unit_converter/` 설명이 공존하면 Agent 혼선 |
| **P0** | Dual-Track 표를 **테스트 경로**까지 갱신: A → `tests/boundary/` · B → `tests/entity/`, `tests/control/` | Harness·Skill·Command 3-way 불일치 |
| **P0** | Logic Track: Entity/Control Mock 금지. UI Track: Control Mock 허용. RED 시 Logic은 `src/boundary/` 수정 금지. | Mock 규칙이 Rule에 없어 `/review-ocp-srp`만 SSOT |
| **P0** | `## 오류 계약 E001~E007`: 코드·조건·exit·출력 채널 표 + U-*/FR-*/D-* C2C 1행씩 | 저장소에 E00x SSOT 없음; Boundary 테스트 Then이 흔들림 |
| **P1** | TDD Phase별 **편집 허용 경로** 표 (RED=`tests/**` only, GREEN=최소 `src`, REFACTOR=Budget) | “구현 금지”만으로는 `src/boundary` vs `src/entity` 구분 불가 |
| **P1** | `## Test/Review Loop`: Phase별 pytest 명령 3줄 + GREEN/REFACTOR 후 결과 보고 의무 | Skill에 Loop 언급만 있고 Rule·Skill 모두 명령 미고정 |
| **P1** | Layer 선언을 `Entity \| Control \| Boundary`로 통일 (기존 `domain/app/infrastructure/cli` 폐기 또는 매핑표) | TDD 선언 한 줄이 ECB와 안 맞음 |
| **P1** | OCP/SRP를 ECB 용어로 재서술: Entity=도메인·레지스트리, Control=유스케이스·변환 흐름, Boundary=CLI·포맷 | NFR 검증 위치가 `domain/converter.py`로 고정돼 있음 |
| **P2** | `## Hook 연동`: Golden Master·`src/**` RED 편집·skip/xfail — **Rule=원칙, Hook=강제**, 승인 토큰 예: `APPROVE_GOLDEN=1` | Hook 도입 시 Rule과 중복·모순 방지 |
| **P2** | `UnitConverter.py`는 레거시 참고만; 신규 코드는 `src/` ECB만 | 금지 사항에 `unit_converter/`만 있어 Harness와 불일치 |
| **P2** | `/review-ocp-srp` 스캔 범위를 `src/**`, `tests/{entity,control,boundary}/`로 교체 | Command가 구 경로 하드코딩 |
| **P3** | README·Report/01·`docs/PRD.md`와 Rule 상단 **상호 링크** | C2C 추적 시 문서 4곳 SSOT 분산 |

---

## 초안에 있으면 좋은 “헌법 한 블록” 예시 (참고용, 수정 아님)

```markdown
## ECB 의존 규칙
- boundary → control → entity (단방향)
- entity는 stdlib·동일 패키지 entity만 import

## Dual-Track
| Track | Layer | Tests | Mock |
| A UI | boundary | tests/boundary/ | control mock 허용 |
| B Logic | entity, control | tests/entity/, tests/control/ | mock 금지 |

## TDD 게이트
- RED: tests/** only, pytest.fail 허용, src/** 금지
- GREEN: RED 1묶음만 src/**, 1 RED = 1 커밋(사용자 요청 시)
- REFACTOR: pytest tests/ -v 전 PASS 후 Budget(파일≤3) 내 REFACTOR only
```

---

## 다음 단계

초안 **전문**을 붙여 주시면 위 표의 P0 항목 기준으로 **문장별 OK/GAP/중복** 표를 추가로 드리겠습니다. 특히 **E001~E007 정의표**와 **Golden Master 승인 문구**가 초안에 어떻게 적혀 있는지가 1차 검증 포인트입니다.

[내용 생략]

---

## User

개선 가능한 부분 개선해줘

---

## Assistant

리뷰에서 지적된 ECB·Dual-Track·SSOT 정렬 항목을 반영하기 위해 관련 파일을 확인합니다.

[내용 생략]

[Tool: Read]
[Tool: Read]
[Tool: Read]
[Tool: Glob]

---

## Assistant

[내용 생략]

[Tool: Read]
[Tool: Read]
[Tool: Read]
[Tool: Read]
[Tool: Read]
[Tool: Read]

---

## Assistant

[내용 생략]

[Tool: Read]
[Tool: Read]

---

## Assistant

[내용 생략]

[Tool: Grep]

---

## Assistant

`.cursorrules`와 Skill·Command·reference를 ECB Harness에 맞춰 정렬합니다.

[내용 생략]

[Tool: Write]
[Tool: Write]

---

## Assistant

[내용 생략]

[Tool: Write]
[Tool: StrReplace]
[Tool: StrReplace]

---

## Assistant

[내용 생략]

[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]

---

## Assistant

[내용 생략]

[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]

---

## Assistant

[내용 생략]

[Tool: Read]
[Tool: Grep]

---

## Assistant

[내용 생략]

[Tool: StrReplace]
[Tool: StrReplace]
[Tool: StrReplace]
[Tool: Shell]

---

## Assistant

[내용 생략]

[Tool: Grep]

---

## Assistant

리뷰에서 지적된 ECB·Dual-Track·SSOT 불일치를 정렬했습니다.

## 변경 요약

### `.cursorrules` (헌법 전면 개편)
- **SSOT 계층** 5단계 명시
- **ECB** 구조 + `boundary → control → entity` import 규칙
- **E001~E007** 오류 계약표 + stderr/exit 계약
- **Dual-Track** ↔ `tests/{entity,control,boundary}/` + Mock 규칙
- **TDD 편집 게이트** + **Test/Review Loop** pytest 명령
- **Hook 연동 원칙** (Golden Master 승인 등)

### `reference.md`
- E001~E007, ECB 컴포넌트 매핑, 레이어별 테스트 디렉터리 반영

### `SKILL.md`
- Layer: `entity|control|boundary`
- Test/Review Loop 표, 파일 결정 규칙, `src/` 경로로 통일

### Commands (6개)
- `red-test-plan`, `red-skeleton`, `green-minimal`, `refactor-smell`, `refactor-safe`, `review-ocp-srp`, `session-export` — ECB 경로·Mock·pytest 예시 갱신

### `README.md` · `docs/PRD.md`
- 프로젝트 구조·CLI·아키텍처 섹션을 `src/` ECB Harness에 맞게 수정

## 아직 하지 않은 것
- **Hook 구현** (`.cursor/hooks.json`) — Rule에 원칙만 기록
- **테스트·src 본문** — Harness 골격 유지
- **`Prompting/`** — 과거 export 기록이라 그대로 둠

`pytest tests/ -v` → `0 items collected` (Harness 정상). 다음 RED부터 `tests/entity/` 등에 스켈레톤을 추가하면 됩니다.

[내용 생략]

---

## User

[Cursor Command: session-export]

/session-export

---
