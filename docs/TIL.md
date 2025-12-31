# Today I Learned

## 2025-12-31

### Python 기본 문법
- `if __name__ == "__main__"`: 직접 실행 vs import 구분
  - 직접 실행 시 `__name__ == "__main__"`
  - import 시 `__name__ == "파일경로"`
  - 테스트 코드 작성할 때 유용
- `==` vs `is`: Python엔 `===` 없음
  - `==`: 값 비교
  - `is`: 객체 비교 (같은 메모리 주소)
- 문법: `{}` 없음 → `:` + 들여쓰기로 블록 구분
- 조건문에 `()` 선택사항
- 파라미터 순서: 필수 → 선택 (기본값 있는 것)
- 네이밍: `snake_case` (함수/변수), `PascalCase` (클래스), `UPPER_CASE` (상수)

### 자료형
- 기본: `str`, `int`, `float`, `bool`, `None`
- 컬렉션: `list`, `dict`, `set`, `tuple`
- `float`만 있음 (double 없음, 64-bit)
- `True`/`False`, `None` (모두 대문자)
- f-string: `f"{name}"` (JS의 템플릿 리터럴)

### Docstring
- `"""설명"""`: 함수 문서화 (Python의 JSDoc)
- `help(함수)`로 확인 가능
- 주석(`#`)과 다름

### Typer
- CLI 도구 만드는 라이브러리 (TypeScript 아님!)
- `typer.run(함수)`: 함수를 CLI로 자동 변환
- 함수명이 `main`일 필요 없음 (아무 이름이나 가능)
- 필수 인자: 순서대로, 선택 인자: `--옵션` (순서 무관)

### 가상환경
- `python3 src/cli.py` ❌ 시스템 Python (패키지 없음)
- `uv run python src/cli.py` ✅ 가상환경 (.venv 사용)
- uv가 자동으로 가상환경 활성화해줌

### 환경 변수
- `load_dotenv()`: .env 파일 → 환경 변수 등록
- `os.getenv("KEY")`: 환경 변수 읽기
- `.env` (비밀, Git 무시) vs `.env.example` (예시, Git 올림)

### HTTP 요청
- `httpx` (현대적, async 지원) vs `requests` (전통적)
- `httpx.post(url, headers={...}, json={...})`
- `json=` 파라미터가 자동 변환 (requests는 `data=json.dumps()` 필요)

### LLM API
- OpenRouter: 무료 LLM 모델 중계
- MiMo-V2-Flash: SWE-bench 1등, 코딩 특화
- Role: `system` (방침), `user` (질문), `assistant` (답변)
- Content: 문자열 (텍스트) vs 배열 (멀티모달: 텍스트+이미지)
- Temperature: 0.0 (일관) ~ 2.0 (창의)

### 프롬프트 엔지니어링
- 마크다운 (범용) vs XML (Claude 최적화)
- 대부분 모델은 둘 다 OK
- 형식보다 구조화 + 명확성이 중요

### Git + Python
- `subprocess.run(['git', 'diff', '--staged'])`: Git 명령어 실행
- `capture_output=True, text=True`: 출력 캡처
- Stage된 변경사항으로 commit 메시지 생성 가능
