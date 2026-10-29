"""Check a running deployment using public HTTP only (creates test games).

Usage: python tests/smoke_deployment.py https://your-service.onrender.com
Not part of unittest discovery: requires a running server and explicit URL.
"""

import json
import string
import sys
import subprocess
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def verify(base_url):
    base_url = base_url.rstrip("/")

    def call(path, body=None):
        request = Request(
            base_url + path,
            data=None if body is None else json.dumps(body).encode(),
            headers={} if body is None else {"Content-Type": "application/json"},
        )
        try:
            response = urlopen(request, timeout=90)
        except HTTPError as exc:
            response = exc
        with response:
            return response.status, json.load(response)

    for path, content_type in (("/", "text/html"), ("/static/app.js", "javascript"),
                               ("/static/style.css", "text/css")):
        with urlopen(base_url + path, timeout=90) as response:
            assert response.status == 200 and content_type in response.headers["Content-Type"]
    ids = set()
    for difficulty in ("easy", "medium", "hard"):
        status, state = call("/api/games", {"difficulty": difficulty})
        assert status == 201 and state["status"] == "playing" and "word" not in state
        assert state["difficulty"] == difficulty and state["remaining_guesses"] == 6
        game_id = state["game_id"]
        assert game_id not in ids
        ids.add(game_id)
        path = f"/api/games/{game_id}"
        assert call(path) == (200, state)
        assert call(path + "/guess", {"letter": "ab"})[0] == 400
        assert call(path) == (200, state)
        # Play only using letter guesses. Do not read server files or an active answer.
        for letter in string.ascii_lowercase:
            status, state = call(path + "/guess", {"letter": letter})
            assert status == 200
            assert call(path) == (200, state)
            if state["status"] != "playing":
                break
            assert "word" not in state
        assert state["status"] in ("won", "lost") and state["word"]
        assert call(path + "/guess", {"letter": "z"})[0] == 409
        assert call(path) == (200, state)
        print(f"{difficulty}: create/get/guess, validation, answer hiding, and {state['status']} verified")
    status, fresh = call("/api/games", {"difficulty": "easy"})
    assert status == 201 and fresh["game_id"] not in ids
    assert fresh["guessed_letters"] == [] and "word" not in fresh
    assert call("/api/games/not-a-real-game")[0] == 404
    print(f"Deployment smoke checks passed: {base_url}")


if __name__ == "__main__":
    if sys.argv[1:] == ["--local-gunicorn"]:
        process = subprocess.Popen([
            sys.executable, "-m", "gunicorn", "--bind", "127.0.0.1:8766",
            "--workers", "1", "--threads", "4", "server:app",
        ])
        try:
            for attempt in range(50):
                if process.poll() is not None:
                    raise RuntimeError("Gunicorn exited before startup.")
                try:
                    with urlopen("http://127.0.0.1:8766/", timeout=1):
                        break
                except OSError:
                    time.sleep(0.1)
            else:
                raise RuntimeError("Gunicorn did not start in time.")
            verify("http://127.0.0.1:8766")
        finally:
            process.terminate()
            process.wait(timeout=10)
        raise SystemExit(0)
    if len(sys.argv) != 2 or not sys.argv[1].startswith(("https://", "http://")):
        raise SystemExit("Usage: python tests/smoke_deployment.py BASE_URL")
    verify(sys.argv[1])
