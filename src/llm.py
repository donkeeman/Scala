import httpx
import json
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
    system_prompt = """You are a senior code reviewer.

**Your job:**
- Review the code diff provided by the user
- Point out bugs, security issues, and performance problems
- Suggest improvements with specific code examples
- Be concise and actionable
- Match the user's language (Korean or English)

**Style:**
- Be direct but respectful
- Focus on important issues, skip nitpicks
- If the code looks good, say so briefly"""

    data = {
    "model": "openrouter/free",
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
    print("[답변]")
    print(content)
    print("\n" + "=" * 50)
    print(f"[토큰] 입력 {usage['prompt_tokens']} / 출력 {usage['completion_tokens']}")

    if reasoning:
        print("\n[추론 과정]")
        print(reasoning)

    return content  # 답변만 반환

if __name__ == "__main__":
    test_diff = """
    def get_user(id):
        query = f"SELECT * FROM users WHERE id = {id}"
        return db.execute(query)
    """
    result = ask_llm(f"다음 코드를 리뷰해줘:\n{test_diff}")
    print(result)