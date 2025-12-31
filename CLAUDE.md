# CLAUDE.md

이 문서는 AI 에이전트(Claude, Cursor, Copilot 등)가 이 프로젝트를 이해하고 
개발을 도와줄 때 참조하는 컨텍스트입니다.

---

## 프로젝트 개요

GitHub PR에 자동으로 코드 리뷰 댓글을 다는 에이전트 봇을 만드는 프로젝트.

### 목표
1. **학습 목적**: AI 에이전트 개념 (RAG, 메모리, 도구 사용 등) 배우기
2. **Python 연습**: TypeScript 개발자가 Python 익히기
3. **프라이버시**: 로컬 LLM으로 코드 외부 전송 없이 동작

---

## 기술 스택

| 영역 | 기술 | 비고 |
|------|------|------|
| 언어 | Python | 학습 목적 |
| LLM | Ollama + Qwen2.5-Coder | 로컬 실행 |
| CLI | Typer | |
| GitHub 연동 | GitHub App + Webhook | PyGithub |
| 벡터 DB | ChromaDB (예정) | RAG용 |

---

## 개발자 프로필

이 프로젝트의 개발자는:
- TypeScript/프론트엔드 개발자 (React, Next.js 숙련)
- Python은 학습 중
- AI/에이전트 개발은 처음

**에이전트에게 요청:**
- Python 코드 작성 시 타입 힌트 적극 사용
- 복잡한 AI 개념은 프론트엔드 개념에 비유해서 설명
- 코드를 대신 짜주기보다 학습할 수 있도록 방향 제시 선호

---

## 현재 진행 상황

> 이 섹션은 개발이 진행되면서 업데이트됩니다.

**현재 Phase:** Phase 1 - 환경 세팅

**완료:**
- [ ] Ollama 설치
- [ ] Python 환경 세팅

**진행 중:**
- (없음)

**다음 단계:**
- Ollama API를 Python으로 호출하기

---

## 프로젝트 구조
ai-code-reviewer/
├── pyproject.toml
├── README.md
├── AGENTS.md (이 파일)
├── docs/
│ └── ROADMAP.md
├── src/
│ ├── init.py
│ ├── cli.py # CLI 엔트리포인트
│ ├── llm.py # Ollama API 래퍼
│ ├── github_app.py # 웹훅 핸들러
│ ├── reviewer.py # 리뷰 생성 로직
│ └── prompts.py # 프롬프트 템플릿
└── tests/


---

## 코딩 컨벤션

- Python 3.11+
- 타입 힌트 필수
- docstring: Google 스타일
- 포매터: ruff
- 패키지 매니저: uv

---

## 참고 문서

- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Typer](https://typer.tiangolo.com/)
- [PyGithub](https://pygithub.readthedocs.io/)
- [GitHub Apps](https://docs.github.com/en/apps)
- [프롬프트 엔지니어링 가이드](https://www.promptingguide.ai/)

---

## 에이전트 지침

이 프로젝트를 도울 때:

1. **학습 중심**: 코드를 바로 작성해주기보다 개념 설명과 방향 제시
2. **점진적 진행**: 한 번에 많은 것을 하지 말고 단계별로
3. **Python 스타일**: Pythonic한 코드 작성법 알려주기
4. **비교 설명**: TypeScript/React 개념과 비교해서 설명하면 이해 빠름