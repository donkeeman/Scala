"""GitHub App Webhook 서버"""
import os
from fastapi import FastAPI, Request, HTTPException
from github import Github, GithubIntegration
from dotenv import load_dotenv
from src.scala import ask_scala

load_dotenv()

app = FastAPI()

# GitHub App 설정 (환경변수에서 로드)
APP_ID = os.getenv("GITHUB_APP_ID")
PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")


def get_github_client(installation_id: int) -> Github:
    """GitHub App 인증으로 클라이언트 생성"""
    with open(PRIVATE_KEY_PATH, "r") as f:
        private_key = f.read()

    integration = GithubIntegration(APP_ID, private_key)
    access_token = integration.get_access_token(installation_id).token
    return Github(access_token)


def get_pr_diff(repo, pr_number: int, max_chars: int = 10000) -> str:
    """PR의 diff 가져오기 (코드 파일만, 크기 제한)"""
    pr = repo.get_pull(pr_number)
    files = pr.get_files()

    # 코드 파일 확장자
    code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs'}

    diff_text = ""
    for file in files:
        # 코드 파일만 포함
        ext = '.' + file.filename.split('.')[-1] if '.' in file.filename else ''
        if ext not in code_extensions:
            continue

        if file.patch:
            diff_text += f"\n### {file.filename}\n"
            diff_text += f"```diff\n{file.patch}\n```\n"

        # 크기 제한
        if len(diff_text) > max_chars:
            diff_text = diff_text[:max_chars] + "\n\n... (diff truncated)"
            break

    if not diff_text:
        return "코드 파일 변경사항 없음"

    return diff_text


def post_review_comment(repo, pr_number: int, review_body: str):
    """PR에 리뷰 코멘트 달기"""
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(review_body)


@app.post("/webhook")
async def handle_webhook(request: Request):
    """GitHub Webhook 핸들러"""
    payload = await request.json()

    # PR 이벤트만 처리
    action = payload.get("action")
    if "pull_request" not in payload:
        return {"status": "ignored", "reason": "not a PR event"}

    # PR 열림/업데이트/재오픈 시에만 리뷰
    if action not in ["opened", "synchronize", "reopened"]:
        return {"status": "ignored", "reason": f"action '{action}' not handled"}

    pr_data = payload["pull_request"]
    pr_number = pr_data["number"]
    repo_full_name = payload["repository"]["full_name"]
    installation_id = payload["installation"]["id"]

    print(f"[Webhook] PR #{pr_number} on {repo_full_name} - action: {action}")

    try:
        # GitHub 클라이언트 생성
        gh = get_github_client(installation_id)
        repo = gh.get_repo(repo_full_name)

        # PR diff 가져오기
        diff = get_pr_diff(repo, pr_number)
        print(f"[Webhook] Got diff ({len(diff)} chars)")

        # Scala로 리뷰 생성
        review = ask_scala("다음 PR의 코드 변경사항을 리뷰해줘", diff)
        print(f"[Webhook] Generated review ({len(review)} chars)")

        # PR에 코멘트 달기
        post_review_comment(repo, pr_number, review)
        print(f"[Webhook] Posted review comment")

        return {"status": "success", "pr": pr_number}

    except Exception as e:
        print(f"[Webhook] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Health check"""
    return {"status": "ok", "message": "Scala Code Review Bot"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
