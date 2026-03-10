"""Scala Bot 통합 시작 스크립트

uvicorn 서버 + cloudflared 터널을 함께 시작하고,
GitHub App webhook URL을 자동으로 업데이트합니다.
"""
import os
import re
import sys
import time
import signal
import subprocess
import httpx
import jwt
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# print 버퍼링 방지
sys.stdout.reconfigure(line_buffering=True)

load_dotenv()

APP_ID = os.getenv("GITHUB_APP_ID")
PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")
SERVER_PORT = 8000


def generate_jwt() -> str:
    """GitHub App JWT 생성"""
    with open(PRIVATE_KEY_PATH, "r") as f:
        private_key = f.read()

    now = datetime.now(timezone.utc)
    payload = {
        "iat": int(now.timestamp()) - 60,
        "exp": int((now + timedelta(minutes=10)).timestamp()),
        "iss": APP_ID,
    }
    return jwt.encode(payload, private_key, algorithm="RS256")


def update_webhook_url(tunnel_url: str):
    """GitHub App의 webhook URL을 업데이트"""
    token = generate_jwt()
    resp = httpx.patch(
        "https://api.github.com/app/hook/config",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        json={"url": f"{tunnel_url}/webhook"},
        timeout=10.0,
    )
    if resp.status_code == 200:
        print(f"[Start] Webhook URL updated: {tunnel_url}/webhook")
    else:
        print(f"[Start] Failed to update webhook URL: {resp.status_code} {resp.text}")


def parse_tunnel_url(output: str) -> str | None:
    """cloudflared 출력에서 터널 URL 추출"""
    match = re.search(r"(https://[a-z0-9-]+\.trycloudflare\.com)", output)
    return match.group(1) if match else None


def main():
    processes: list[subprocess.Popen] = []

    def cleanup(sig=None, frame=None):
        print("\n[Start] Shutting down...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.wait(timeout=5)
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    # 1. uvicorn 서버 시작
    print(f"[Start] Starting server on port {SERVER_PORT}...")
    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.github_app:app",
         "--host", "0.0.0.0", "--port", str(SERVER_PORT)],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    processes.append(server)
    time.sleep(2)

    # 2. cloudflared 터널 시작
    print("[Start] Starting cloudflared tunnel...")
    tunnel = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", f"http://localhost:{SERVER_PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    processes.append(tunnel)

    # 3. 터널 URL 파싱 (stderr에서 읽음)
    tunnel_url = None
    deadline = time.time() + 30
    collected = ""
    while time.time() < deadline:
        line = tunnel.stderr.readline()
        if not line:
            break
        decoded = line.decode("utf-8", errors="replace")
        collected += decoded
        url = parse_tunnel_url(collected)
        if url:
            tunnel_url = url
            break

    if not tunnel_url:
        print("[Start] Failed to get tunnel URL")
        cleanup()
        return

    print(f"[Start] Tunnel URL: {tunnel_url}")

    # 4. GitHub webhook URL 자동 업데이트
    update_webhook_url(tunnel_url)

    print("[Start] Ready! Press Ctrl+C to stop.")

    # 서버 프로세스가 끝날 때까지 대기
    try:
        server.wait()
    except KeyboardInterrupt:
        cleanup()


if __name__ == "__main__":
    main()
