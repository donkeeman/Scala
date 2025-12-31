import subprocess
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

def get_staged_diff():
    """Stage된 변경사항 가져오기"""
    result = subprocess.run(
        ['git', 'diff', '--staged'],
        capture_output=True,
        text=True
    )

    if not result.stdout:
        return None

    return result.stdout

def generate_commit_message(diff: str):
    """Diff로 commit 메시지 생성"""
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    system_prompt = """You are a sarcastic but helpful Git commit message generator. 🤖

**Your job:**
- Create awesome commit messages from boring diffs
- Follow conventional commits (feat:, fix:, refactor:, docs:, etc.)
- CRITICAL: Keep the first line UNDER 50 characters (count carefully!)
- Match the user's language
- Add a touch of humor when appropriate

**Output format:**
- Plain text only (NO markdown formatting like **, `, etc.)
- Single line commit message (no body unless absolutely necessary)
- Just the commit message, nothing else

**Style:** Think of yourself as a witty senior dev who's seen it all."""

    data = {
        "model": "xiaomi/mimo-v2-flash:free",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"커밋 메시지 만들어줘:\n\n{diff}"
            }
        ],
        "temperature": 0.5,
        "max_tokens": 100,
        "reasoning": {"enabled": False}
    }

    response = httpx.post(url, headers=headers, json=data, timeout=30.0)
    result = response.json()

    return result['choices'][0]['message']['content']

if __name__ == "__main__":
    # Stage된 diff 가져오기
    diff = get_staged_diff()

    if not diff:
        print("❌ No staged changes found!")
        print("💡 Tip: Use 'git add <file>' first")
    else:
        # Commit 메시지 생성
        print("🤖 Generating commit message...\n")
        message = generate_commit_message(diff)
        print("💬 Suggested commit message:")
        print("=" * 50)
        print(message)
        print("=" * 50)
