# /session-export — 회고 보고서·Transcript Export·README 갱신

UnitConverter_29 **실습 회고** — `Report/`에 보고서를 생성하고, `Prompting/`에 Agent Transcript를 **번호 순**으로 Export한 뒤 `README.md`를 갱신한다.

## 필수 선언

**응답 첫 줄**에 아래 형식을 반드시 선언한다:

```
Phase: export | Scope: session-report | Track: Documentation
```

---

## 산출물

| 폴더 | 파일 패턴 | 설명 |
|------|-----------|------|
| `Report/` | `NNN-회고-보고서.md` | 실습 회고·달성도·AI 활용 요약 (한국어) |
| `Prompting/` | `NNN-<주제-slug>.md` | Agent 대화 Transcript (번호·시간순) |
| `README.md` | — | Commands·폴더 구조·회고 섹션 갱신 |

번호 `NNN`은 **001부터** 3자리 zero-padding. **기존 파일이 있으면** 최대 번호 다음부터 이어서 매긴다.

---

## 절차

### 1. Transcript 수집

Agent Transcript 원본 경로 (Cursor 프로젝트별):

```
%USERPROFILE%\.cursor\projects\c-DEV-UnitConverter-29\agent-transcripts\**\*.jsonl
```

- `*.jsonl` 전부 탐색 (Glob 또는 Shell).
- **수정 시각 오름차순** 정렬 (가장 오래된 세션 = 001).
- 현재 세션(이 `/session-export` 실행 중인 대화)도 포함한다.

### 2. `Prompting/` Export

각 Transcript를 **읽기 쉬운 Markdown**으로 변환해 저장한다.

**파일명**: `Prompting/NNN-<주제-slug>.md`

- `<주제-slug>`: 첫 user 메시지에서 `<user_query>` 본문을 kebab-case 영문 또는 짧은 한글 (공백·특수문자 제거, 40자 이내).
- 예: `001-venv-setup.md`, `002-gitignore-commit.md`, `003-cursor-commands.md`

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
| 중복 Export | 동일 Session ID가 이미 `Prompting/`에 있으면 **덮어쓰지 않고** 번호·내용 비교 후 갱신 여부 판단 |

### 3. `Report/` 보고서 생성

**파일명**: `Report/NNN-회고-보고서.md` (보통 `001`; 재실행 시 `002` …)

`README.md` **「5. 회고 및 발표」** 항목을 충실히 반영한다:

```markdown
# UnitConverter 실습 회고 보고서

- **작성일**: YYYY-MM-DD
- **프로젝트**: UnitConverter_29
- **Transcript 수**: N개 (`Prompting/` 참조)

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
| 001 | [001-…](Prompting/001-….md) | … | … | … |

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

- 저장소 상태 스캔: `unit_converter/`, `tests/`, `pytest` 결과
- `Prompting/` 파일 목록과 상호 링크
- 추측이 아닌 **Transcript·코드·pytest 근거** 기반 서술

### 4. `README.md` 갱신

기존 내용은 유지하고, 아래 섹션을 **추가 또는 갱신**한다 (중복 제거).

#### 4-a. Cursor Commands 표

| Command | 파일 | 용도 |
|---------|------|------|
| `/red-test-plan` | `.cursor/commands/red-test-plan.md` | RED 설계표 |
| `/red-skeleton` | `.cursor/commands/red-skeleton.md` | RED 테스트 스켈레톤 |
| `/green-minimal` | `.cursor/commands/green-minimal.md` | GREEN 최소 구현 |
| `/refactor-smell` | `.cursor/commands/refactor-smell.md` | 스멜 분석 |
| `/refactor-safe` | `.cursor/commands/refactor-safe.md` | Safe Refactor |
| `/review-ocp-srp` | `.cursor/commands/review-ocp-srp.md` | OCP/SRP·C2C 리뷰 |
| `/session-export` | `.cursor/commands/session-export.md` | **회고 보고서·Transcript Export** |

#### 4-b. 산출물 폴더

```markdown
### 산출물 폴더

| 폴더 | 내용 |
|------|------|
| `Report/` | 실습 회고 보고서 (`NNN-회고-보고서.md`) |
| `Prompting/` | Cursor Agent 대화 Transcript Export (`NNN-*.md`) |

회고 정리: 채팅에서 `/session-export` 실행.
```

#### 4-c. 「5. 회고 및 발표」

- `Report/` 최신 보고서 링크
- `Prompting/` Transcript 목록 (번호·파일명·한 줄 요약) 테이블

### 5. 완료 보고

채팅에 아래 형식으로 보고한다:

```markdown
## Session Export 완료

- **Report**: Report/001-회고-보고서.md
- **Prompting**: N개 Export (001 ~ 00N)
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
| **git commit** (명시 요청 없을 때) | 사용자 요청 시만 |

---

## 참고

- 실습 Activities: `README.md` 「생성형AI를 활용한 Activities」
- TDD SSOT: `.cursor/skills/unit-converter-tdd/SKILL.md`
- Test ID: `.cursor/skills/unit-converter-tdd/reference.md`
