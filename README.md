
## Unit Converter (Python)
![unit-converter](./unit-converter.jpg)

### Overview
- 사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 다른 모든 단위로 변환해 출력하는 프로그램.
- 새로운 단위를 추가할 때 기존 코드의 변경이 최소화되도록 설계한다.
- 각 단위 변환 로직은 테스트 코드로 검증한다.

### 문제 정의 (Mom Test)
- **진짜 문제**: 해외 스펙과 국내 실측·발주 단위가 섞인 상태에서 확실한 기준 없이 수동 계산·해석을 반복하다 시간·오차·책임 리스크가 반복 발생한다.
- **주제 (한 문장)**: 해외 스펙과 국내 실측·발주 단위가 섞일 때, 손 계산·해석 반복으로 잃는 시간과 틀린 숫자 비용을, **한 번 입력으로 여러 단위를 일관되게 맞추는 것**으로 줄인다.

| 문서 | 설명 |
|------|------|
| [`Report/01.UnitConverter_ProblemDefinition_Report.md`](Report/01.UnitConverter_ProblemDefinition_Report.md) | Mom Test 인터뷰 · R-G-I-O · 성공 기준 |
| [`docs/PRD.md`](docs/PRD.md) | FR / NFR / EXT · C2C · 수용 기준 |
| [`.cursor/skills/unit-converter-tdd/reference.md`](.cursor/skills/unit-converter-tdd/reference.md) | Test ID · Given/Then SSOT |

### 프로젝트 구조

```
UnitConverter_29/
├── UnitConverter.py          # 레거시 시드 (분석용)
├── unit_converter/           # 목표 패키지 (TDD로 구현)
│   ├── domain/
│   ├── infrastructure/
│   ├── app/
│   └── cli.py
├── tests/
│   ├── test_cli.py           # Track A (U-*)
│   └── test_converter.py     # Track B (D-*)
├── docs/PRD.md
├── Report/
└── .cursor/                  # Commands · Skill · Rules
```

### 가상환경 설정 및 실행
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 의존성 (pytest 등)
pip install -r requirements.txt

# 레거시 실행
python UnitConverter.py

# 목표 CLI (구현 후)
python -m unit_converter "meter:2.5"

# 테스트
python -m pytest tests/ -v

# 가상환경 비활성화
deactivate
```

### 기본 요구사항
1. 사용자 입력 예시:
   ```
   meter:2.5
   ```
   → 출력:
   ```
   2.5 meter = 8.2 feet
   2.5 meter = 2.7 yard
   ...
   ```

2. 현재 지원 단위:
   - meter
   - feet
   - yard

3. 새로운 단위가 추가될 때도 기존 코드의 변경이 최소화되도록 할 것.

4. 각 단위 간 변환이 정확히 계산되도록 테스트 코드를 작성할 것.

### 비즈니스 로직
- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간의 비율은 meter 기반으로 계산.

### 품질 요구사항
- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)

### 추가 요구사항
- **설정 외부화**
   - 변환 비율을 외부 설정 파일(JSON/YAML)에서 로드
- **동적으로 단위와 비율을 등록할 수 있도록 한다**
   - 사용자 입력으로 `1 cubit = 0.4572 meter`를 등록하고 사용 가능
- **출력 포맷 선택 기능**
   - JSON / CSV / 표 형태 출력

### Cursor Commands

| Command | 파일 | 용도 |
|---------|------|------|
| `/red-test-plan` | `.cursor/commands/red-test-plan.md` | RED 설계표 |
| `/red-skeleton` | `.cursor/commands/red-skeleton.md` | RED 테스트 스켈레톤 |
| `/green-minimal` | `.cursor/commands/green-minimal.md` | GREEN 최소 구현 |
| `/refactor-smell` | `.cursor/commands/refactor-smell.md` | 스멜 분석 |
| `/refactor-safe` | `.cursor/commands/refactor-safe.md` | Safe Refactor |
| `/review-ocp-srp` | `.cursor/commands/review-ocp-srp.md` | OCP/SRP·C2C 리뷰 |
| `/session-export` | `.cursor/commands/session-export.md` | 회고 보고서·Transcript Export |

TDD 절차 SSOT: [`.cursor/skills/unit-converter-tdd/SKILL.md`](.cursor/skills/unit-converter-tdd/SKILL.md)

### 산출물 폴더

| 폴더 | 내용 |
|------|------|
| `docs/` | PRD · 설계 문서 |
| `Report/` | 문제 정의 · 실습 회고 보고서 |
| `Prompting/` | Cursor Agent 대화 Transcript Export |

회고 정리: 채팅에서 `/session-export` 실행.

## 생성형AI를 활용한 Activities (6 시간)

1. 문제 코드 및 기본 요구사항 분석 (0.5시간)
   - 기본 코드구조, 로직 이해
   - Mom Test · R-G-I-O · [`Report/01`](Report/01.UnitConverter_ProblemDefinition_Report.md) · [`docs/PRD.md`](docs/PRD.md)
2. 기본 요구사항 및 품질 요구사항 구현 (2시간)
   - OCP를 만족하는 인터페이스 구현
   - SRP를 만족하도록 클래스 구현
   - 입력값 검증을 위한 구현
3. TC 구현 (0.5시간)
   - 단위변환 기능 검증 및 입력 값 검증 TC 작성
4. 추가 요구사항 구현 (2시간)
   - 3개 요구사항 구현 및 TC 작성
5. 회고 및 발표 (1시간)
   - 실습 목표와 달성도
   - AI를 어떻게 활용했나? 도움이 된 순간과 한계는?
   - TC를 추가해보면서 개선에 미친 영향, TC 작성 팁
   - 클린코드와 리팩토링에서 느낀 장점과 어려운점
   - 회고 보고서: `Report/` ( `/session-export` )
