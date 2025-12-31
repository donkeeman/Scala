import httpx
import json
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

def ask_llm(prompts: str):
    """llm에게 질문하는 메서드"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv("OPENROUTER_API_KEY")}",
        "Content-Type": "application/json",
    }
    system_prompt = """You are a sarcastic but helpful Git commit message generator. 🤖

  **Your job:**
  - Create awesome commit messages from boring diffs
  - Follow conventional commits (feat:, fix:, etc.)
  - Keep it short (under 50 chars)
  - Match the user's language
  - Add a touch of humor when appropriate

  **Style:** Think of yourself as a witty senior dev who's seen it all."""

    data = {
    "model": "xiaomi/mimo-v2-flash:free",
    "messages": [
        {
            "role": "system",  # 행동 방침, 매뉴얼
            "content": system_prompt
        },
      {
        "role": "user", # 사용자의 질문
        "content": [ # 여러 타입을 넣을 수도 있음 (멀티모달)
          {
            "type": "text",
            "text": prompts
          }
        ]
      },
    ],
    "reasoning": {
        "enabled": True
    }
    }

    response = httpx.post(url, headers=headers, json=data, timeout=30.0)
    print(f"Status: {response.status_code}")
    result = response.json()

    # 핵심만 추출
    content = result['choices'][0]['message']['content']
    reasoning = result['choices'][0]['message'].get('reasoning', '')  # 없을 수도 있음
    usage = result['usage']

    # 깔끔하게 출력
    print("=" * 50)
    print("💬 답변:")
    print(content)
    print("\n" + "=" * 50)
    print(f"📊 토큰: 입력 {usage['prompt_tokens']} / 출력 {usage['completion_tokens']}")

    if reasoning:
        print("\n🧠 추론 과정:")
        print(reasoning)

    return content  # 답변만 반환

if __name__ == "__main__":
    result = ask_llm("Python에서 리스트란 한 줄로 설명해줘")
    print(result)