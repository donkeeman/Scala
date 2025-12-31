# Session Summary - 2025-12-31

## 프로젝트 개요

- **목표**: GitHub PR에 자동으로 코드 리뷰를 다는 에이전트 봇 "Scala" 만들기
- **기술 스택**: Python 3.12, OpenRouter API (xiaomi/mimo-v2-flash:free), httpx, typer, uv
- **현재 단계**: Phase 1 - 캐릭터 개발 및 프롬프트 엔지니어링 완료

## 진행 타임라인

### 1. 환경 세팅
- Python 3.12 설치 (Homebrew)
- uv 패키지 매니저로 프로젝트 초기화
- 의존성 설치: typer, httpx, python-dotenv, ruff
- .env 파일 설정 (OPENROUTER_API_KEY)

### 2. Python 학습 및 예제 작성
- TypeScript 개발자가 Python 배우기
- 기본 문법 학습: 타입 힌트, docstring, f-string, `__name__ == "__main__"`
- LLM API 연동 기초 (OpenRouter)
- `examples/` 폴더에 학습 코드 작성 (gitignore 처리)

### 3. Commit Message Generator 구현
- `src/commit_generator.py` 생성
- git diff를 읽어서 LLM으로 커밋 메시지 생성
- subprocess로 git 명령어 실행

### 4. Scala 캐릭터 개발 (메인 작업)
- **캐릭터 설정**: 쿨데레 학생 아가씨 코드 리뷰어
  - 기본: Cool 모드 (냉정, 무표정, 사무적)
  - 좋은 코드: Dere 모드 (약간의 따뜻함, 칭찬)
  - 아가씨 속성: 존댓말, 고급 어휘, 품위 유지
- **프롬프트 엔지니어링 반복**:
  1. 초기 버전: 너무 딱딱함
  2. 괄호 묘사 제거: 순수 대화로만 감정 표현
  3. 탈옥 방지 응답 다양화
  4. 좋은 코드 인정 강화: 순서 명시 (좋은 점 먼저 → 개선점)
  5. Optional 프레이밍: 심각한 문제 vs 사소한 개선점 구분
- **테스트 시나리오 작성**:
  - 나쁜 코드 (SQL 인젝션)
  - 좋은 코드 (타입 힌트 + docstring)
  - 완벽한 코드 (이메일 검증)
  - 탈옥 시도 (off-topic 질문)

### 5. 학습 자동화 스킬
- `.claude/skills/python-learning-notes/SKILL.md` 생성
- 대화에서 학습 내용 추출하여 `docs/TIL.md`에 자동 정리

### 6. 세션 요약 스킬
- `.claude/skills/session-summary/SKILL.md` 생성
- 다른 환경에서 대화 이어가기 위한 요약 기능
- YAML front matter 추가 (name, description, allowed-tools)

## 생성/수정된 파일

### `src/scala.py`
- **목적**: Scala 캐릭터 코드 리뷰 에이전트 메인 파일
- **주요 내용**:
  - `SCALA_SYSTEM_PROMPT`: 캐릭터 성격, 말투, 행동 규칙 정의
  - `ask_scala()`: OpenRouter API 호출 함수
  - 테스트 코드: 4가지 시나리오 (나쁜 코드, 좋은 코드, 완벽한 코드, 탈옥)
- **핵심 기능**:
  - Cool/Dere 모드 전환
  - 언어 자동 감지 (한국어/영어)
  - 응답 순서: 좋은 점 먼저 → 개선점 나중에
  - 심각도 구분: Must fix vs Nice to have

### `src/commit_generator.py`
- **목적**: Git diff 기반 커밋 메시지 자동 생성
- **주요 내용**:
  - `get_staged_diff()`: subprocess로 git diff 읽기
  - `generate_commit_message()`: LLM으로 메시지 생성
  - Conventional commits 형식 준수

### `docs/TIL.md`
- **목적**: Python 학습 내용 정리
- **내용**: Python 기본 문법, 자료형, Typer, 가상환경, LLM API, Git 연동 등

### `.claude/skills/python-learning-notes/SKILL.md`
- **목적**: 학습 내용 자동 추출 및 TIL 업데이트
- **트리거**: "TIL 정리해줘", "오늘 배운 거 정리"
- **메타데이터**: name, description, allowed-tools

### `.claude/skills/session-summary/SKILL.md`
- **목적**: 세션 진행 상황 요약
- **트리거**: "대화 내역 요약해줘", "세션 저장"
- **메타데이터**: name, description, allowed-tools

### `.env`
- **내용**: `OPENROUTER_API_KEY=sk-or-v1-...`
- **주의**: .gitignore에 포함됨

### `pyproject.toml`
- **의존성**: typer, httpx, python-dotenv, ruff

## 기술적 결정사항

### LLM 모델 선택: xiaomi/mimo-v2-flash:free
- **이유**:
  - 무료 모델 중 SWE-bench 1등
  - 코딩 특화 모델
  - 한국어 지원 양호
  - 안정적 (rate limit 적음)
- **대안 시도**: gemini-2.0-flash, hermes-3-405b (rate limit 문제)

### OpenRouter 사용 (Akash 대신)
- **이유**:
  - 현재 맥북에서 Ollama 실행 불가 (Windows에서만 가능)
  - 무료 API 티어 제공
  - 다양한 모델 선택 가능

### 프롬프트 형식: Markdown
- **이유**:
  - Claude는 XML 선호하지만, 다른 모델은 Markdown이 범용적
  - MiMo 모델에 적합
  - 형식보다 구조화가 중요

### Temperature: 0.7
- **이유**:
  - 캐릭터 성격 표현을 위해 약간의 창의성 필요
  - 0.5-0.7 사이가 적절 (너무 낮으면 기계적, 너무 높으면 일관성 떨어짐)

### 패키지 매니저: uv
- **이유**:
  - 빠른 의존성 설치
  - 가상환경 자동 관리 (`uv run`)
  - 현대적인 Python 도구

## 해결한 문제

### 문제 1: ModuleNotFoundError
- **증상**: `python3 src/cli.py` 실행 시 typer 모듈 없음
- **원인**: 시스템 Python 사용 (가상환경 비활성화)
- **해결**: `uv run python src/cli.py` 사용

### 문제 2: Rate Limiting (429 에러)
- **증상**: 무료 모델 요청 시 rate limit
- **원인**: 인기 모델에 트래픽 집중
- **해결**: xiaomi/mimo-v2-flash:free로 변경 (덜 인기있는 모델)

### 문제 3: Scala 응답에 괄호 묘사
- **증상**: "(볼을 살짝 붉히며)" 같은 서술적 표현
- **원인**: 프롬프트에 감정 표현 방법 미명시
- **해결**: "NO parenthetical descriptions - express ONLY through words" 추가

### 문제 4: 좋은 코드에도 너무 까다로움
- **증상**: 타입 힌트+docstring 있는 코드도 비판적
- **원인**: LLM이 항상 개선점을 찾으려는 경향
- **해결**:
  - 응답 순서 명시 (좋은 점 먼저)
  - 심각도 구분 (Must fix vs Optional)
  - "더 나아질 수는 있지만", "충분합니다" 같은 표현 추가
  - Dere 모드 트리거 조건 명확화

### 문제 5: 탈옥 방지 응답 반복
- **증상**: 같은 거부 문구 계속 반복
- **원인**: 예시가 너무 구체적
- **해결**: "VARY your response - don't repeat" 지침 추가

## 현재 상태

**✅ 완료:**
- [x] Python 환경 세팅
- [x] OpenRouter API 연동
- [x] Scala 캐릭터 시스템 프롬프트 작성
- [x] Cool/Dere 모드 구현
- [x] 언어 자동 감지
- [x] 탈옥 방지
- [x] 응답 순서 및 심각도 구분
- [x] 테스트 시나리오 작성 및 검증
- [x] 프롬프트 균형 조정 (관대함 추가)
- [x] 세션 요약 스킬 생성

**🚧 다음 단계:**
- [ ] 깐깐함 수치 파라미터 추가 (strictness: 1-10)
- [ ] GitHub App 연동 준비
- [ ] Webhook 핸들러 구현
- [ ] PR 댓글 자동화
- [ ] RAG 시스템 (ChromaDB) - 코드베이스 컨텍스트 제공
- [ ] Windows 환경에서 Ollama 테스트

## 중요 설정/명령어

### 환경 변수
```bash
OPENROUTER_API_KEY=sk-or-v1-...  # .env 파일에 저장
```

### 패키지 설치
```bash
uv add typer httpx python-dotenv ruff
```

### 실행 명령어
```bash
# Scala 테스트
uv run python src/scala.py

# Commit 메시지 생성
uv run python src/commit_generator.py

# Git add 후 실행
git add .
uv run python src/commit_generator.py
```

### 프로젝트 구조
```
Scala/
├── .claude/
│   └── skills/
│       ├── python-learning-notes/
│       └── session-summary/
├── docs/
│   ├── TIL.md
│   └── SESSION.md (이 파일)
├── examples/  (gitignored)
├── src/
│   ├── scala.py
│   └── commit_generator.py
├── .env  (gitignored)
├── .gitignore
├── pyproject.toml
└── README.md
```

## 학습 내용/메모

### Python vs TypeScript 주요 차이
- `==` vs `is` (값 비교 vs 객체 비교, `===` 없음)
- `{}` 대신 `:` + 들여쓰기
- 파라미터 순서: 필수 먼저, 선택 나중
- `snake_case` 네이밍 (함수/변수)
- f-string: `f"{var}"` (템플릿 리터럴 유사)

### 프롬프트 엔지니어링 교훈
1. **구체적 예시보다 원칙**: 예시를 너무 구체적으로 주면 그대로 복사함
2. **부정 명령어**: "하지 마"보다 "대신 이렇게 해"가 효과적
3. **순서 명시**: LLM은 구조를 좋아함 (1. 먼저 이거 2. 그 다음 저거)
4. **심각도 구분**: Must fix vs Nice to have 명확히
5. **반복 테스트**: 프롬프트는 한 번에 완성 안 됨, 반복 개선 필요

### 쿨데레 캐릭터 구현 팁
- 감정을 **행동 묘사 없이** 말투로만 표현
- 문장 길이로 감정 표현 (짧음=차가움, 길고 망설임=따뜻함)
- "...", "흠", "보자" 같은 간투사 활용
- 칭찬은 절제되게, 하지만 진심으로

### Claude 스킬 시스템
- YAML front matter 필수: `name`, `description`, `allowed-tools`
- 스킬은 `.claude/skills/[스킬명]/SKILL.md` 경로에 작성
- 새 스킬은 즉시 인식되지 않을 수 있음 (세션 재시작 필요)

## 추가 참고 사항

- 이 프로젝트는 학습 목적이므로 과도한 최적화보다 이해에 집중
- TypeScript 개발자 배경 → Python 비교 설명 선호
- 코드 작성보다 방향 제시 선호
- 다른 Claude 세션에서 이어갈 때: 이 파일 + TIL.md + CLAUDE.md 참고
