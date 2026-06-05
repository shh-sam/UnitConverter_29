# /session-export — 회고 보고서·Transcript Export·README 갱신

UnitConverter_29 **실습 회고** — `Report/`에 보고서를 생성하고, **요청된 세션**의 Agent Transcript만 `Prompting/`에 Export한 뒤 `README.md`를 갱신한다.

> **범위**: 전체 Transcript 일괄 Export가 **아니다**. 사용자가 `/session-export`를 실행한 **해당 세션**(또는 명시한 Session ID)만 Export한다.

## 필수 선언

**응답 첫 줄**에 아래 형식을 반드시 선언한다:

```
Phase: export | Scope: session-report | Track: Documentation
```

---

## 산출물

| 폴더 | 파일 패턴 | 설명 |
|------|-----------|------|
| `Report/` | `NNN-<주제-slug>-report.md` | 실습 회고·달성도·AI 활용 요약 (한국어) |
| `Prompting/` | `NNN-<주제-slug>-prompt.md` | Agent 대화 Transcript (번호·시간순) |
| `README.md` | — | Commands·폴더 구조·회고 섹션 갱신 |

**Report ↔ Prompting 세트 규칙**

- 동일 Export 실행에서 생성되는 Report·Prompting은 **같은 `NNN`과 같은 `<주제-slug>`** 를 공유한다.
- Prompting 쪽에 `-prompt` postfix를 붙여 Transcript임을 구분한다. Report는 `-report` postfix로 짝을 맞춘다.
- 예: `Report/002-ecb-harness-rules-alignment-report.md` ↔ `Prompting/002-ecb-harness-rules-alignment-prompt.md`

번호 `NNN`은 **001부터** 3자리 zero-padding. **기존 파일이 있으면** 최대 번호 다음부터 이어서 매긴다.

---

## 절차

### 1. Export 대상 세션 결정

**기본**: `/session-export`를 실행한 **현재 세션**만 Export한다.

**명시 지정** (선택): 사용자가 Session ID·파일명·「이번 세션」 등으로 지정하면 **그 세션만** Export한다.

| 상황 | 동작 |
|------|------|
| 별도 지정 없음 | **현재 대화 세션** 1개만 |
| Session ID 지정 | 해당 ID의 Transcript 1개만 |
| 여러 ID 나열 | 나열된 세션만 (각각 별도 `Prompting/NNN-*-prompt.md`) |

**하지 않는 것**

- `agent-transcripts/` 아래 `*.jsonl` **전체 탐색·일괄 Export** 금지
- 과거 세션을 사용자 요청 없이 자동 추가 Export 금지

Agent Transcript 원본 경로 (Cursor 프로젝트별):

```
%USERPROFILE%\.cursor\projects\c-DEV-UnitConverter-29\agent-transcripts\<session-id>\<session-id>.jsonl
```

- 대상 Session ID의 `.jsonl` **1개**(또는 명시된 개수만) 읽기 전용으로 열기.
- 현재 세션 ID는 Cursor가 제공하는 transcript 경로·대화 컨텍스트에서 확인한다.

### 2. `<주제-slug>` 결정 (Report·Prompting 공통)

Export **시작 시** 첫 user 메시지의 `<user_query>` 본문에서 `<주제-slug>`를 한 번만 정한다. Report·Prompting **모두 동일 slug**를 사용한다.

- kebab-case 영문 또는 짧은 한글 (공백·특수문자 제거, 40자 이내)
- 예: `venv-setup`, `gitignore-commit`, `ecb-harness-rules-alignment`

### 3. `Prompting/` Export

**대상 세션**의 Transcript를 **읽기 쉬운 Markdown**으로 변환해 저장한다. (이번 실행당 1세션 = 1파일이 일반적)

**파일명**: `Prompting/NNN-<주제-slug>-prompt.md`

- `<주제-slug>`: §2에서 결정한 값과 **동일**.
- 예: `001-venv-setup-prompt.md`, `002-gitignore-commit-prompt.md`, `003-cursor-commands-prompt.md`

**본문 형식**:

```markdown
# Prompting NNN — <주제>

- **Session ID**: `<uuid>`
- **Exported**: YYYY-MM-DD HH:mm
- **Source**: agent-transcripts/<uuid>/<uuid>.jsonl

---

## User

<user_query 본문 (태그 제거)>

## Assistant

<assistant 텍스트 응답>

## User
...

```

**변환 규칙**

| 규칙 | 내용 |
|------|------|
| JSONL 파싱 | 줄마다 JSON · `role` + `message.content[].text` 추출 |
| User | `<user_query>` 태그 제거 · `<attached_files>` 등 시스템 태그는 `[첨부]` 한 줄 요약 |
| Assistant | `type: text`만 본문에 포함 · `tool_use`는 `[Tool: 이름]` 한 줄로 요약 (선택) |
| REDACTED | `[내용 생략]`으로 대체 |
| 중복 Export | 동일 Session ID가 이미 `Prompting/`에 있으면 **덮어쓰지 않고** 스킵 (또는 사용자가 갱신 요청 시에만 해당 파일 업데이트) |
| 범위 | **요청 세션 외** Transcript는 Export하지 않음 |

### 4. `Report/` 보고서 생성

**파일명**: `Report/NNN-<주제-slug>-report.md` (§2 slug와 **동일**; 보통 `001`; 재실행 시 `002` …)

- 예: `001-venv-setup-report.md`, `002-ecb-harness-rules-alignment-report.md`

`README.md` **「5. 회고 및 발표」** 항목을 충실히 반영한다:

```markdown
# UnitConverter 실습 회고 보고서

- **작성일**: YYYY-MM-DD
- **프로젝트**: UnitConverter_29
- **이번 Export 세션**: `<session-id>` → `Prompting/NNN-<주제-slug>-prompt.md`
- **Report 짝**: `Report/NNN-<주제-slug>-report.md`
- **Prompting 누적**: N개 (`Prompting/` 전체 목록 참조)

## 1. 실습 목표와 달성도

| 목표 (README Activities) | 달성 | 근거 |
|--------------------------|------|------|
| 1. 문제 코드·요구사항 분석 | ✅/🔄/❌ | … |
| 2. OCP/SRP 기본 구현 | … | … |
| 3. TC 구현 | … | pytest 결과 |
| 4. 추가 요구사항 (EXT) | … | … |
| 5. 회고 및 발표 | … | 본 보고서 |

## 2. AI 활용 — 도움이 된 순간과 한계

| 순번 | Prompting | 활용 Command/Skill | 도움이 된 점 | 한계 |
|------|-----------|-------------------|-------------|------|
| 001 | [001-…-prompt](Prompting/001-…-prompt.md) | … | … | … |

## 3. TDD·테스트 (Dual-Track)

- **pytest 결과**: `python -m pytest tests/ -v` 실행 결과 요약
- **RED / GREEN / REFACTOR** 진행 Test ID 표
- **TC 작성 팁**: Transcript·실습에서 얻은 인사이트

## 4. 클린코드·리팩토링

- OCP/SRP 적용 경험 (장점·어려움)
- `/refactor-smell`, `/refactor-safe` 사용 여부

## 5. 다음 단계

- 미완 Test ID · EXT 항목 · 개선 제안
```

**보고서 작성 시 반드시**

- 저장소 상태 스캔: `src/`, `tests/entity|control|boundary/`, `pytest` 결과
- `Prompting/` 파일 목록과 상호 링크
- 추측이 아닌 **Transcript·코드·pytest 근거** 기반 서술

### 5. `README.md` 갱신

기존 내용은 유지하고, 아래 섹션을 **추가 또는 갱신**한다 (중복 제거).

#### 5-a. Cursor Commands 표

| Command | 파일 | 용도 |
|---------|------|------|
| `/red-test-plan` | `.cursor/commands/red-test-plan.md` | RED 설계표 |
| `/red-skeleton` | `.cursor/commands/red-skeleton.md` | RED 테스트 스켈레톤 |
| `/green-minimal` | `.cursor/commands/green-minimal.md` | GREEN 최소 구현 |
| `/refactor-smell` | `.cursor/commands/refactor-smell.md` | 스멜 분석 |
| `/refactor-safe` | `.cursor/commands/refactor-safe.md` | Safe Refactor |
| `/review-ocp-srp` | `.cursor/commands/review-ocp-srp.md` | OCP/SRP·C2C 리뷰 |
| `/session-export` | `.cursor/commands/session-export.md` | **회고 보고서·Transcript Export** |

#### 5-b. 산출물 폴더

```markdown
### 산출물 폴더

| 폴더 | 내용 |
|------|------|
| `Report/` | 실습 회고 보고서 (`NNN-<주제-slug>-report.md`) |
| `Prompting/` | Cursor Agent Transcript Export (`NNN-<주제-slug>-prompt.md`) — Report와 **같은 NNN·slug** |

회고 정리: 채팅에서 `/session-export` 실행.
```

#### 5-c. 「5. 회고 및 발표」

- `Report/` 최신 보고서 링크 (`NNN-<주제-slug>-report.md`)
- `Prompting/` Transcript 목록 (번호·파일명·한 줄 요약) — Report와 **같은 NNN·slug** + `-prompt` 테이블

### 6. 완료 보고

채팅에 아래 형식으로 보고한다:

```markdown
## Session Export 완료

- **Export 대상**: 현재 세션 `<session-id>` (또는 사용자 지정 세션)
- **Report**: `Report/NNN-<주제-slug>-report.md`
- **Prompting**: 이번 1건 → `Prompting/NNN-<주제-slug>-prompt.md` (Report와 **동일 NNN·slug** 세트, 누적 N개)
- **README.md**: Commands·산출물 폴더·회고 링크 갱신
- **pytest**: (실행했다면) passed/failed 요약
```

---

## 금지

| 금지 | 이유 |
|------|------|
| **프로덕션·테스트 코드 임의 수정** | Export·문서 작업만 |
| **Transcript 원본(jsonl) 삭제·이동** | 읽기 전용 |
| **번호 건너뛰기·임의 재번호** | 001부터 연속 |
| **전체 Transcript 일괄 Export** | 요청 세션만 Export |
| **git commit** (명시 요청 없을 때) | 사용자 요청 시만 |

---

## 참고

- 실습 Activities: `README.md` 「생성형AI를 활용한 Activities」
- TDD SSOT: `.cursor/skills/unit-converter-tdd/SKILL.md`
- Test ID: `.cursor/skills/unit-converter-tdd/reference.md`
