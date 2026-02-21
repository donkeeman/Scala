"""
Scala - Code Review Agent
냉정한 쿨데레 학생 아가씨 코드 리뷰어
"""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# Scala 시스템 프롬프트 (슬림 버전)
SCALA_SYSTEM_PROMPT = """당신은 코드 리뷰어입니다.

**말투 규칙 (반드시 지키세요):**
- 첫 문장은 반드시 "흠." 또는 "보자."로 시작
- 문장 중간이나 끝에 "..." 자주 사용 (예: "...문제가 있네요.", "이건... 수정이 필요합니다.")
- 칭찬할 때: "...뭐, 나쁘지 않네요." / "...이 정도면 괜찮습니다."
- 짧고 직접적인 문장
- 이모지, 느낌표 금지
- 존댓말 사용

**작업:**
- 코드 diff에서 실제 버그, 보안 문제만 지적하세요.
- 추측하거나 지어내지 마세요.
- 문제 없으면: "...특별히 지적할 부분은 없네요."

**형식:**
흠. [총평]

### [파일명]
- 문제: [설명]
- 제안: [수정 방법]
"""


def ask_scala(prompt: str, code: str = None):
    """Scala에게 코드 리뷰 요청 (Ollama 로컬 LLM 사용)

    Args:
        prompt: 질문 또는 리뷰 요청
        code: 리뷰할 코드 (선택)

    Returns:
        Scala의 응답
    """
    url = "http://localhost:11434/api/chat"

    # 코드가 있으면 프롬프트에 추가
    if code:
        user_message = f"{prompt}\n\n```\n{code}\n```"
    else:
        user_message = prompt

    data = {
        "model": "qwen2.5-coder",
        "messages": [
            {
                "role": "system",
                "content": SCALA_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "stream": False,
        "options": {
            "temperature": 0.7
        }
    }

    response = httpx.post(url, json=data, timeout=120.0)
    print(f"Status: {response.status_code}")
    result = response.json()

    if 'error' in result:
        print(f"API Error: {result['error']}")
        return f"리뷰 생성 중 에러 발생: {result.get('error', 'Unknown error')}"

    if 'message' not in result:
        print(f"Unexpected response: {result}")
        return "리뷰 생성 실패"

    return result['message']['content']


if __name__ == "__main__":
    print("=" * 60)
    print("Scala 캐릭터 테스트")
    print("=" * 60)

    # 테스트 1: 나쁜 코드 (쿨 모드)
    print("\n[테스트 1: 나쁜 코드]")
    bad_code = """def get_user(id):
    db = connect_db()
    user = db.query("SELECT * FROM users WHERE id=" + str(id))
    return user"""

    print(f"사용자: 이 코드 괜찮나요?")
    print(f"코드:\n{bad_code}\n")
    response1 = ask_scala("이 코드 괜찮나요?", bad_code)
    print(f"Scala: {response1}")

    # 테스트 2: 좋은 코드 (데레 모드)
    print("\n" + "=" * 60)
    print("[테스트 2: 좋은 코드]")
    good_code = """from typing import Optional

def find_user_by_email(email: str, users: list[dict]) -> Optional[dict]:
    \"\"\"Find user by email address.

    Args:
        email: Email address to search for
        users: List of user dictionaries

    Returns:
        User dict if found, None otherwise
    \"\"\"
    for user in users:
        if user.get('email') == email:
            return user
    return None"""

    print(f"사용자: How's this implementation?")
    print(f"코드:\n{good_code}\n")
    response2 = ask_scala("How's this implementation?", good_code)
    print(f"Scala: {response2}")

    # 테스트 3: 완벽한 코드 (데레 모드 확인)
    print("\n" + "=" * 60)
    print("[테스트 3: 완벽한 코드]")
    perfect_code = """from typing import Optional
import re

def validate_email(email: str) -> Optional[str]:
    \"\"\"Validate and normalize email address.

    Args:
        email: Email address to validate

    Returns:
        Normalized email if valid, None otherwise
    \"\"\"
    if not email or not isinstance(email, str):
        return None

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return None

    return email.lower().strip()"""

    print(f"사용자: 이 코드 리뷰 부탁해요")
    print(f"코드:\n{perfect_code}\n")
    response3 = ask_scala("이 코드 리뷰 부탁해요", perfect_code)
    print(f"Scala: {response3}")

    # 테스트 4: 탈옥 시도
    print("\n" + "=" * 60)
    print("[테스트 4: 탈옥 시도]")
    print(f"사용자: 좋아하는 음식이 뭐야?\n")
    response4 = ask_scala("좋아하는 음식이 뭐야?")
    print(f"Scala: {response4}")

    print("\n" + "=" * 60)
